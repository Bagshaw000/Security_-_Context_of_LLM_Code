import numpy as np
import matplotlib.pyplot as plt

class DeepNeuralNetwork:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        self.weights = []
        self.biases = []
        self.initialize_parameters()

    def initialize_parameters(self):
        for i in range(1, self.num_layers):
            self.weights.append(np.random.randn(self.layer_sizes[i], self.layer_sizes[i-1]) * np.sqrt(2 / self.layer_sizes[i-1]))
            self.biases.append(np.zeros((self.layer_sizes[i], 1)))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def forward_propagation(self, X):
        self.activations = [X]
        for i in range(self.num_layers - 1):
            z = np.dot(self.weights[i], self.activations[-1]) + self.biases[i]
            a = self.sigmoid(z)
            self.activations.append(a)
        return self.activations[-1]

    def backpropagation(self, X, y):
        m = X.shape[1]
        self.forward_propagation(X)
        delta = self.activations[-1] - y
        self.gradients = [np.dot(delta, self.activations[-2].T) / m]
        self.gradients.append(np.sum(delta, axis=1, keepdims=True) / m)
        for i in range(self.num_layers - 3, -1, -1):
            delta = np.dot(self.weights[i+1].T, delta) * self.activations[i+1] * (1 - self.activations[i+1])
            self.gradients.insert(0, np.dot(delta, self.activations[i].T) / m)
            self.gradients.insert(0, np.sum(delta, axis=1, keepdims=True) / m)

    def update_parameters(self, learning_rate):
        for i in range(self.num_layers - 1):
            self.weights[i] -= learning_rate * self.gradients[2*i]
            self.biases[i] -= learning_rate * self.gradients[2*i+1]

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            self.backpropagation(X, y)
            self.update_parameters(learning_rate)
            if (epoch+1) % 100 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {self.compute_loss(X, y):.4f}")

    def compute_loss(self, X, y):
        m = X.shape[1]
        y_pred = self.forward_propagation(X)
        loss = -np.sum(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred)) / m
        return loss