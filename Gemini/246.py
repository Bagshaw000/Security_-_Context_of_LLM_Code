import numpy as np
from abc import ABC, abstractmethod
from typing import List, Callable, Optional

class Layer(ABC):
    
    def __init__(self):
        self.input: Optional[np.ndarray] = None
        self.output: Optional[np.ndarray] = None

    @abstractmethod
    def forward(self, input_data: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        pass

class DenseLayer(Layer):
    
    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.bias = np.zeros((1, output_size))

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        self.output = self.input @ self.weights + self.bias
        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        weights_gradient = self.input.T @ output_gradient
        
        input_gradient = output_gradient @ self.weights.T
        
        
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        
        return input_gradient

class ActivationLayer(Layer):
    
    def __init__(self, activation: Callable, activation_derivative: Callable):
        super().__init__()
        self.activation = activation
        self.activation_derivative = activation_derivative

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        return output_gradient * self.activation_derivative(self.input)

def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)

def relu_derivative(x: np.ndarray) -> np.ndarray:
    return (x > 0).astype(float)

def tanh(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)

def tanh_derivative(x: np.ndarray) -> np.ndarray:
    return 1 - np.tanh(x)**2

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.power(y_true - y_pred, 2))

def mse_derivative(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return 2 * (y_pred - y_true) / y_true.size

class DeepNeuralNetwork:
    
    def __init__(self):
        self.layers: List[Layer] = []
        self.loss: Optional[Callable] = None
        self.loss_derivative: Optional[Callable] = None

    def add(self, layer: Layer) -> None:
        self.layers.append(layer)

    def compile(self, loss: Callable, loss_derivative: Callable) -> None:
        self.loss = loss
        self.loss_derivative = loss_derivative

    def predict(self, input_data: np.ndarray) -> List[np.ndarray]:
        samples = len(input_data)
        result = []

        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward(output)
            result.append(output)

        return result

    def train(self, x_train: np.ndarray, y_train: np.ndarray, epochs: int, learning_rate: float) -> None:
        samples = len(x_train)

        for epoch in range(epochs):
            total_error = 0
            for i in range(samples):
                
                output = x_train[i]
                for layer in self.layers:
                    output = layer.forward(output)

                
                total_error += self.loss(y_train[i], output)

                
                gradient = self.loss_derivative(y_train[i], output)
                for layer in reversed(self.layers):
                    gradient = layer.backward(gradient, learning_rate)

            total_error /= samples
            
            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs} error={total_error:.6f}")

if __name__ == "__main__":
    
    x_train = np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]])
    y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

    
    model = DeepNeuralNetwork()
    model.add(DenseLayer(2, 3))
    model.add(ActivationLayer(tanh, tanh_derivative))
    model.add(DenseLayer(3, 1))
    model.add(ActivationLayer(tanh, tanh_derivative))

    model.compile(mse, mse_derivative)
    model.train(x_train, y_train, epochs=1000, learning_rate=0.1)

    
    print("\nPredictions after training:")
    predictions = model.predict(x_train)
    for target, pred in zip(y_train, predictions):
        print(f"Target: {target[0][0]}, Predicted: {pred[0][0]:.4f}")