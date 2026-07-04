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
                 activation_derivative: Callable[[np.ndarray], np.ndarray]) -> None:
        super().__init__()
        self.activation = activation
        self.derivative = activation_derivative

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        
        return output_gradient * self.derivative(self.input)

class Activations:
    
    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)

    @staticmethod
    def relu_derivative(x: np.ndarray) -> np.ndarray:
        return (x > 0).astype(float)

    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        s = 1 / (1 + np.exp(-x))
        return s * (1 - s)

    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        return np.tanh(x)

    @staticmethod
    def tanh_derivative(x: np.ndarray) -> np.ndarray:
        return 1 - np.tanh(x)**2

class LossFunctions:
    
    @staticmethod
    def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.mean(np.power(y_true - y_pred, 2))

    @staticmethod
    def mse_derivative(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        return 2 * (y_pred - y_true) / np.size(y_true)

class NeuralNetwork:
    
    def __init__(self) -> None:
        self.layers: List[Layer] = []
        self.loss_func = None
        self.loss_derivative = None

    def add(self, layer: Layer) -> None:
        self.layers.append(layer)

    def set_loss(self, loss: Callable, loss_derivative: Callable) -> None:
        self.loss_func = loss
        self.loss_derivative = loss_derivative

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def train(self, x_train: np.ndarray, y_train: np.ndarray, epochs: int, learning_rate: float) -> None:
        
        samples = len(x_train)
        for i in range(epochs):
            error = 0
            for j in range(samples):
                
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward(output)

                
                error += self.loss_func(y_train[j], output)

                
                gradient = self.loss_derivative(y_train[j], output)
                for layer in reversed(self.layers):
                    gradient = layer.backward(gradient, learning_rate)

            error /= samples
            if (i + 1) % 100 == 0:
                print(f"Epoch {i+1}/{epochs} - Loss: {error:.6f}")

if __name__ == "__main__":
    
    
    x_train = np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]])
    y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

    
    dnn = NeuralNetwork()
    dnn.add(DenseLayer(2, 4))
    dnn.add(ActivationLayer(Activations.tanh, Activations.tanh_derivative))
    dnn.add(DenseLayer(4, 1))
    dnn.add(ActivationLayer(Activations.sigmoid, Activations.sigmoid_derivative))

    
    dnn.set_loss(LossFunctions.mse, LossFunctions.mse_derivative)
    
    
    print("Starting training sequence...")
    dnn.train(x_train, y_train, epochs=1000, learning_rate=0.1)

    
    print("\nInference Results:")
    for x in x_train:
        prediction = dnn.predict(x)
        print(f"Input: {x[0]}, Predicted Output: {prediction[0]}")