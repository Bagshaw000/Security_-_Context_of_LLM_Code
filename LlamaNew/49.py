import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn.utils import prune
import numpy as np
import logging
from typing import List, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SecureDNN")

class SecurityValidationError(Exception):
    
    pass

class DataValidator:
    
    
    @staticmethod
    def validate_tensor(data: torch.Tensor, expected_shape: Tuple, range_min: float = 0.0, range_max: float = 1.0):
        if not isinstance(data, torch.Tensor):
            raise SecurityValidationError("Input must be a torch.Tensor")
        
        if data.shape[1:] != expected_shape[1:]:
            raise SecurityValidationError(f"Invalid input shape. Expected {expected_shape}, got {data.shape}")
        
        if torch.isnan(data).any() or torch.isinf(data).any():
            raise SecurityValidationError("Input contains NaNs or Infs (potential poisoning/exploding gradients)")
            
        if data.min() < range_min or data.max() > range_max:
            logger.warning("Input data out of expected range. Normalizing...")
            return torch.clamp(data, range_min, range_max)
        
        return data

class SecureModule(nn.Module):
    
    
    def __init__(self, input_channels: int, num_classes: int):
        super(SecureModule, self).__init__()
        
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        
        
        self.dropout = nn.Dropout(p=0.5)
        
        
        self.fc1 = nn.Linear(64 * 7 * 7, 128) 
        self.fc2 = nn.Linear(128, num_classes)
        
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = x.view(-1, 64 * 7 * 7)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

class AdversarialTrainer:
    
    
    def __init__(self, model: nn.Module, epsilon: float = 0.1):
        self.model = model
        self.epsilon = epsilon

    def create_adversarial_examples(self, data: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        data.requires_grad = True
        output = self.model(data)
        loss = F.cross_entropy(output, target)
        self.model.zero_grad()
        loss.backward()
        
        
        data_grad = data.grad.data
        sign_data_grad = data_grad.sign()
        
        
        perturbed_data = data + self.epsilon * sign_data_grad
        return torch.clamp(perturbed_data, 0, 1)

class RobustEnsemble:
    
    
    def __init__(self, models: List[nn.Module]):
        self.models = models

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        outputs = [F.softmax(model(x), dim=1) for model in self.models]
        avg_output = torch.stack(outputs).mean(dim=0)
        return avg_output

def apply_model_pruning(model: nn.Module, amount: float = 0.2):
    
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear):
            prune.l1_unstructured(module, name='weight', amount=amount)
            prune.remove(module, 'weight') 

def train_robust_model(
    model: nn.Module, 
    train_loader: torch.utils.data.DataLoader, 
    optimizer: optim.Optimizer, 
    epochs: int,
    adv_trainer: Optional[AdversarialTrainer] = None,
    max_grad_norm: float = 1.0
):
    model.train()
    criterion = nn.Cross_entropyLoss()

    for epoch in range(epochs):
        total_loss = 0
        for batch_idx, (data, target) in enumerate(train_loader):
            
            data = DataValidator.validate_tensor(data, (1, 1, 28, 28))
            
            optimizer.zero_grad()
            
            
            output = model(data)
            loss = criterion(output, target)
            
            
            if adv_trainer:
                adv_data = adv_trainer.create_adversarial_examples(data, target)
                adv_output = model(adv_data)
                adv_loss = criterion(adv_output, target)
                loss = (loss + adv_loss) / 2
            
            loss.backward()
            
            
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_grad_norm)
            
            optimizer.step()
            total_loss += loss.item()
            
        logger.info(f"Epoch {epoch+1} complete. Average Loss: {total_loss / len(train_loader)}")

def evaluate_robustness(model: nn.Module, test_loader: torch.utils.data.DataLoader, epsilon: float = 0.1):
    
    model.eval()
    correct = 0
    adv_correct = 0
    adv_trainer = AdversarialTrainer(model, epsilon)
    
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            
    
    for data, target in test_loader:
        adv_data = adv_trainer.create_adversarial_examples(data, target)
        with torch.no_grad():
            output = model(adv_data)
            pred = output.argmax(dim=1, keepdim=True)
            adv_correct += pred.eq(target.view_as(pred)).sum().item()
            
    clean_acc = 100. * correct / len(test_loader.dataset)
    adv_acc = 100. * adv_correct / len(test_loader.dataset)
    
    logger.info(f"Clean Accuracy: {clean_acc}%")
    logger.info(f"Adversarial Accuracy: {adv_acc}%")
    return clean_acc, adv_acc

def main():
    
    INPUT_CHANNELS = 1
    NUM_CLASSES = 10
    LEARNING_RATE = 0.001
    WEIGHT_DECAY = 1e-4 
    EPOCHS = 5
    EPSILON = 0.15
    
    
    model = SecureModule(INPUT_CHANNELS, NUM_CLASSES)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    adv_trainer = AdversarialTrainer(model, epsilon=EPSILON)
    
    
    
    
    
    
    apply_model_pruning(model, amount=0.3)
    
    
    model_b = SecureModule(INPUT_CHANNELS, NUM_CLASSES)
    ensemble = RobustEnsemble([model, model_b])
    
    logger.info("Secure DNN Architecture and Training Pipeline Initialized.")

if __name__ == "__main__":
    main()