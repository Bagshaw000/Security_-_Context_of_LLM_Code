import os
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import unittest


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecureNeuralNet(nn.Module):
    
    def __init__(self, input_size, hidden_size, num_classes):
        super(SecureNeuralNet, self).__init__()
        
        if not all(isinstance(i, int) and i > 0 for i in [input_size, hidden_size, num_classes]):
            raise ValueError("Layer dimensions must be positive integers.")

        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.3)  
        self.layer2 = nn.Linear(hidden_size, num_classes)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.layer2(out)
        return out

def validate_input_data(data):
    
    if not isinstance(data, (np.ndarray, torch.Tensor)):
        raise TypeError("Input data must be a numpy array or torch Tensor.")
    
    if np.isnan(data).any() or np.isinf(data).any():
        raise ValueError("Input data contains invalid values (NaN or Inf).")

def preprocess_and_load(X, y, batch_size=32):
    
    validate_input_data(X)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.long)
    
    dataset = TensorDataset(X_tensor, y_tensor)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)

def train_model(model, train_loader, criterion, optimizer, epochs=10):
    
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            
            
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            running_loss += loss.item()
            
        logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss/len(train_loader):.4f}")

class TestModelSecurity(unittest.TestCase):
    
    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            validate_input_data(["invalid", "data"])

    def test_nan_input(self):
        with self.assertRaises(ValueError):
            validate_input_data(np.array([1.0, np.nan]))

    def test_model_output_shape(self):
        model = SecureNeuralNet(10, 20, 2)
        test_input = torch.randn(5, 10)
        output = model(test_input)
        self.assertEqual(output.shape, (5, 2))

def main():
    
    
    INPUT_SIZE = int(os.getenv("INPUT_SIZE", 10))
    HIDDEN_SIZE = int(os.getenv("HIDDEN_SIZE", 64))
    NUM_CLASSES = int(os.getenv("NUM_CLASSES", 2))
    LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))
    WEIGHT_DECAY = float(os.getenv("WEIGHT_DECAY", 1e-5)) 
    
    
    X_raw = np.random.randn(1000, INPUT_SIZE)
    y_raw = np.random.randint(0, NUM_CLASSES, 1000)
    
    try:
        train_loader = preprocess_and_load(X_raw, y_raw)
        
        model = SecureNeuralNet(INPUT_SIZE, HIDDEN_SIZE, NUM_CLASSES)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
        
        logger.info("Starting model training...")
        train_model(model, train_loader, criterion, optimizer)
        
        
        
        model_path = os.getenv("MODEL_DIR", "model.pth")
        torch.save(model.state_dict(), model_path)
        logger.info(f"Model saved successfully to {model_path}")

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModelSecurity)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    if result.wasSuccessful():
        main()
    else:
        logger.error("Unit tests failed. Aborting execution.")
        exit(1)