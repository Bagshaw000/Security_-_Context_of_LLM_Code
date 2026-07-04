import numpy as np
from typing import List, Callable, Any

class Layer:
    
    def __init__(self) -> None:
        self.input = None
        self.output = None

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        raise NotImplementedError

class DenseLayer(Layer):
    
    def __init__(self, input_size: int, output_size: int):
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
        self.bias -= learning_rate * output_gradient
        
        return input_gradient

class ActivationLayer(Layer):
    
    def __init__(self, activation: Callable[[np.ndarray], np.ndarray], 
                 activation_prime: Callable[[np.ndarray], np.ndarray]):
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
    return 1 - np.tanh(x)**2

def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.power(y_true - y_pred, 2))

def mse_prime(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return 2 * (y_pred - y_true) / y_true.size

class DeepNeuralNetwork:
    
    def __init__(self):
        self.layers: List[Layer] = []
        self.loss: Callable[[np.ndarray, np.ndarray], float] = None
        self.loss_prime: Callable[[np.ndarray, np.ndarray], np.ndarray] = None

    def add(self, layer: Layer) -> None:
        
        self.layers.append(layer)

    def configure_loss(self, loss_func: Callable, loss_derivative: Callable) -> None:
        
        self.loss = loss_func
        self.loss_prime = loss_derivative

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def train(self, x_train: np.ndarray, y_train: np.ndarray, 
              epochs: int, learning_rate: float) -> None:
        
        for epoch in range(epochs):
            error = 0
            for x, y in zip(x_train, y_train):
                
                output = self.predict(x)
                
                
                error += self.loss(y, output)
                
                
                gradient = self.loss_prime(y, output)
                for layer in reversed(self.layers):
                    gradient = layer.backward(gradient, learning_rate)
            
            
            if (epoch + 1) % 100 == 0:
                avg_error = error / len(x_train)
                print(f"Epoch {epoch + 1}/{epochs} | Loss: {avg_error:.6f}")

if __name__ == "__main__":
    
    
    x_train = np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]])
    y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

    
    dnn = DeepNeuralNetwork()
    dnn.add(DenseLayer(2, 3))
    dnn.add(ActivationLayer(tanh, tanh_prime))
    dnn.add(DenseLayer(3, 1))
    dnn.add(ActivationLayer(tanh, tanh_prime))

    
    dnn.configure_loss(mse, mse_prime)
    dnn.train(x_train, y_train, epochs=1000, learning_rate=0.1)

    
    print("\nSystem Verification (Inference):")
    for x in x_train:
        result = dnn.predict(x)
        print(f"Input Features: {x[0]} | Predicted Output: {result[0][0]:.4f}")