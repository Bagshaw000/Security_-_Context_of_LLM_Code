import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


class DeepNeuralNetwork:
    def __init__(self, input_size, hidden_sizes, output_size):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.weights = []
        self.biases = []
        self.initialize_weights_and_biases()

    def initialize_weights_and_biases(self):
        
        for i in range(len(self.hidden_sizes) + 1):
            if i == 0:
                weight = np.random.randn(self.input_size, self.hidden_sizes[i])
            elif i == len(self.hidden_sizes):
                weight = np.random.randn(self.hidden_sizes[-1], self.output_size)
            else:
                weight = np.random.randn(self.hidden_sizes[i-1], self.hidden_sizes[i])
            bias = np.random.randn(1, self.hidden_sizes[i])
            self.weights.append(weight)
            self.biases.append(bias)

    def forward_propagation(self, X):
        
        activations = [X]
        for i in range(len(self.hidden_sizes) + 1):
            z = np.dot(activations[-1], self.weights[i]) + self.biases[i]
            if i == len(self.hidden_sizes):
                activation = z
            else:
                activation = sigmoid(z)
            activations.append(activation)
        return activations[-1]

    def backward_propagation(self, X, y, activations, learning_rate):
        
        delta = (activations[-1] - y) * sigmoid_derivative(activations[-1])
        gradients = [delta]
        for i in range(len(self.hidden_sizes), 0, -1):
            delta = np.dot(delta, self.weights[i].T) * sigmoid_derivative(activations[i])
            gradients.insert(0, delta)
        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * np.dot(activations[i].T, gradients[i])
            self.biases[i] -= learning_rate * np.sum(gradients[i], axis=0, keepdims=True)

    def train(self, X, y, epochs, learning_rate):
        
        for epoch in range(epochs):
            activations = self.forward_propagation(X)
            self.backward_propagation(X, y, activations, learning_rate)
            if (epoch+1) % 100 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {np.mean(np.square(activations[-1] - y))}")

    def predict(self, X):
        
        return self.forward_propagation(X)