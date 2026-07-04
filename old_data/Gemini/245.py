import numpy as np
from typing import List, Callable, Optional

class Layer:
    
    def __init__(self) -> None:
        self.input: Optional[np.ndarray] = None
        self.output: Optional[np.ndarray] = None

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Forward pass must be implemented by subclass.")

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        raise NotImplementedError("Backward pass must be implemented by subclass.")

class DenseLayer(Layer):
    
    def __init__(self, input_size: int, output_size: int) -> None:
        super().__init__()
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.bias = np.zeros((1, output_size))

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        weights_gradient = np.dot(self.input.T, output_gradient)
        input_gradient = np.dot(output_gradient, self.weights.T)
        
        
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * np.sum(output_gradient, axis=0, keepdims=True)
        
        return input_gradient

class ActivationLayer(Layer):
    
    def __init__(self, activation: Callable, activation_prime: Callable) -> None:
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        return self.activation(self.input)

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient * self.activation_prime(self.input)

def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)

def relu_prime(x: np.ndarray) -> np.ndarray:
    return (x > 0).astype(float)

def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(x: np.ndarray) -> np.ndarray:
    s = sigmoid(x)
    return s * (1 - s)

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.power(y_true - y_pred, 2))

def mse_prime(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return 2 * (y_pred - y_true) / y_true.size

class DeepNeuralNetwork:
    
    def __init__(self) -> None:
        self.layers: List[Layer] = []
        self.loss: Optional[Callable] = None
        self.loss_prime: Optional[Callable] = None

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def set_loss_function(self, loss: Callable, loss_prime: Callable) -> None:
        self.loss = loss
        self.loss_prime = loss_prime

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def train(self, x_train: np.ndarray, y_train: np.ndarray, epochs: int, learning_rate: float) -> None:
        
        n_samples = len(x_train)
        for epoch in range(epochs):
            total_error = 0
            for x, y in zip(x_train, y_train):
                
                output = self.predict(x)
                total_error += self.loss(y, output)
                
                
                gradient = self.loss_prime(y, output)
                for layer in reversed(self.layers):
                    gradient = layer.backward(gradient, learning_rate)
            
            if (epoch + 1) % 100 == 0:
                avg_error = total_error / n_samples
                print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_error:.6f}")

if __name__ == "__main__":
    
    
    
    X = np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]])
    Y = np.array([[[0]], [[1]], [[1]], [[0]]])

    model = DeepNeuralNetwork()
    
    
    model.add_layer(DenseLayer(2, 8))
    model.add_layer(ActivationLayer(relu, relu_prime))
    
    
    model.add_layer(DenseLayer(8, 4))
    model.add_layer(ActivationLayer(relu, relu_prime))
    
    
    model.add_layer(DenseLayer(4, 1))
    model.add_layer(ActivationLayer(sigmoid, sigmoid_prime))

    model.set_loss_function(mse, mse_prime)
    
    print("Starting Training...")
    model.train(X, Y, epochs=1000, learning_rate=0.1)

    print("\nValidation Results:")
    for x in X:
        prediction = model.predict(x)
        print(f"Input: {x.flatten()} -> Output: {prediction.flatten()[0]:.4f}")