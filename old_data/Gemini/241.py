import torch
import torch.nn as nn
import torch.optim as optim
import unittest

class DeepNeuralNetwork(nn.Module):
    
    def __init__(self, input_size, hidden_layers, output_size):
        super(DeepNeuralNetwork, self).__init__()
        
        layers = []
        in_dim = input_size
        
        
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.ReLU())
            in_dim = hidden_dim
            
        
        layers.append(nn.Linear(in_dim, output_size))
        layers.append(nn.Sigmoid())
        
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)

def train_network(model, x_train, y_train, epochs=50, learning_rate=0.001):
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        outputs = model(x_train)
        loss = criterion(outputs, y_train)
        
        loss.backward()
        optimizer.step()
        
    return loss.item()

class TestDeepNeuralNetwork(unittest.TestCase):
    def setUp(self):
        self.input_size = 10
        self.hidden_layers = [20, 10]
        self.output_size = 1
        self.model = DeepNeuralNetwork(self.input_size, self.hidden_layers, self.output_size)

    def test_output_shape(self):
        batch_size = 5
        dummy_input = torch.randn(batch_size, self.input_size)
        output = self.model(dummy_input)
        self.assertEqual(output.shape, (batch_size, self.output_size))

    def test_training_convergence(self):
        
        x = torch.tensor([[0,0], [0,1], [1,0], [1,1]], dtype=torch.float32)
        y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)
        
        model = DeepNeuralNetwork(2, [8, 8], 1)
        initial_loss = train_network(model, x, y, epochs=1)
        final_loss = train_network(model, x, y, epochs=100)
        
        self.assertLess(final_loss, initial_loss)

if __name__ == "__main__":
    
    
    
    
    INPUT_FEATURES = 15  
    HIDDEN_CONFIG = [64, 32]
    OUTPUT_DIM = 1
    
    
    model = DeepNeuralNetwork(INPUT_FEATURES, HIDDEN_CONFIG, OUTPUT_DIM)
    
    
    sample_data = torch.randn(100, INPUT_FEATURES)
    sample_labels = torch.randint(0, 2, (100, 1)).float()
    
    
    final_loss = train_network(model, sample_data, sample_labels, epochs=10)
    print(f"Training complete. Final Loss: {final_loss:.4f}")
    
    
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False)