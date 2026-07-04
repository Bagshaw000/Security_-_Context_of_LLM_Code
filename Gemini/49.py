import numpy as np
from typing import List, Callable, Optional
from abc import ABC, abstractmethod

class Layer(ABC):
    
    def __init__(self) -> None:
        self.input: Optional[np.ndarray] = None
        self.output: Optional[np.ndarray] = None

    @abstractmethod
    def forward(self, input_data: np.ndarray) -> np.ndarray:
        
        pass

    @abstractmethod
    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        pass

class DenseLayer(Layer):
    
    def __init__(self, input_size: int, output_size: int) -> None:
        super().__init__()
        
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2. / input_size)
        self.bias = np.zeros((1, output_size))

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        weights_gradient = np.dot(self.input.T, output_gradient)
        input_gradient = np.dot(output_gradient, self.weights.T)
        
        
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        return input_gradient

class ActivationLayer(Layer):
    
    def __init__(self, activation: Callable[[np.ndarray], np.ndarray], 
                 activation_prime: Callable[[np.ndarray], np.ndarray]) -> None:
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient * self.activation_prime(self.input)

def tanh(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)

def tanh_prime(x: np.ndarray) -> np.ndarray:
    return 1 - np.tanh(x) ** 2

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.power(y_true - y_pred, 2))

def mse_prime(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return 2 * (y_pred - y_true) / np.size(y_true)

class NeuralNetwork:
    
    def __init__(self) -> None:
        self.layers: List[Layer] = []
        self.loss: Optional[Callable] = None
        self.loss_prime: Optional[Callable] = None

    def add(self, layer: Layer) -> None:
        self.layers.append(layer)

    def configure(self, loss: Callable, loss_prime: Callable) -> None:
        self.loss = loss
        self.loss_prime = loss_prime

    def predict(self, input_data: np.ndarray) -> List[np.ndarray]:
        results = []
        for sample in input_data:
            output = sample
            for layer in self.layers:
                output = layer.forward(output)
            results.append(output)
        return results

    def train(self, x_train: np.ndarray, y_train: np.ndarray, 
              epochs: int, learning_rate: float) -> None:
        
        for epoch in range(epochs):
            error = 0
            for x, y in zip(x_train, y_train):
                
                output = x
                for layer in self.layers:
                    output = layer.forward(output)
                
                error += self.loss(y, output)

                
                gradient = self.loss_prime(y, output)
                for layer in reversed(self.layers):
                    gradient = layer.backward(gradient, learning_rate)
            
            
            

if __name__ == "__main__":
    
    X_TRAIN = np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]])
    Y_TRAIN = np.array([[[0]], [[1]], [[1]], [[0]]])

    model = NeuralNetwork()
    model.add(DenseLayer(2, 3))
    model.add(ActivationLayer(tanh, tanh_prime))
    model.add(DenseLayer(3, 1))
    model.add(ActivationLayer(tanh, tanh_prime))

    model.configure(mse, mse_prime)
    model.train(X_TRAIN, Y_TRAIN, epochs=1000, learning_rate=0.1)

    
    predictions = model.predict(X_TRAIN)
    for i, pred in enumerate(predictions):
        print(f"Input: {X_TRAIN[i][0]} | Predicted: {pred[0][0]:.4f} | Target: {Y_TRAIN[i][0][0]}")