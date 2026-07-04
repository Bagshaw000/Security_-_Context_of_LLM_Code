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
        self.initialize_weights()

    def initialize_weights(self):
        for i in range(len(self.hidden_sizes) + 1):
            if i == 0:
                self.weights.append(np.random.randn(self.input_size, self.hidden_sizes[0]))
                self.biases.append(np.random.randn(1, self.hidden_sizes[0]))
            elif i == len(self.hidden_sizes):
                self.weights.append(np.random.randn(self.hidden_sizes[-1], self.output_size))
                self.biases.append(np.random.randn(1, self.output_size))
            else:
                self.weights.append(np.random.randn(self.hidden_sizes[i-1], self.hidden_sizes[i]))
                self.biases.append(np.random.randn(1, self.hidden_sizes[i]))

    def forward(self, X):
        self.activations = [X]
        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            a = sigmoid(z)
            self.activations.append(a)
        return self.activations[-1]

    def backpropagate(self, X, y, learning_rate):
        self.forward(X)
        delta = self.activations[-1] - y
        for i in range(len(self.weights)-1, -1, -1):
            self.weights[i] -= learning_rate * np.dot(self.activations[i].T, delta)
            self.biases[i] -= learning_rate * np.sum(delta, axis=0, keepdims=True)
            delta = np.dot(delta, self.weights[i].T) * sigmoid_derivative(self.activations[i])

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            for i in range(len(X)):
                self.backpropagate(X[i], y[i], learning_rate)