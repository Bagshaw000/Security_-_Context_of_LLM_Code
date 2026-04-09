import numpy as np

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input_data):
        raise NotImplementedError

    def backward(self, output_error, learning_rate):
        raise NotImplementedError

class DenseLayer(Layer):
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    def forward(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)

        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error

class ActivationLayer(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def backward(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error

def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1 - np.tanh(x)**2

def mse(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))

def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size

class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    def add(self, layer):
        self.layers.append(layer)

    def set_loss(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    def predict(self, input_data):
        samples = len(input_data)
        result = []
        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward(output)
            result.append(output)
        return result

    def train(self, x_train, y_train, epochs, learning_rate):
        samples = len(x_train)
        for i in range(epochs):
            display_error = 0
            for j in range(samples):
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward(output)

                display_error += self.loss(y_train[j], output)
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward(error, learning_rate)
            
            display_error /= samples
            if (i + 1) % 100 == 0:
                print(f'Epoch {i+1}/{epochs}  Error={display_error:.6f}')

def run_example():
    
    x_train = np.array([[[0,0]], [[0,1]], [[1,0]], [[1,1]]])
    y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

    
    net = NeuralNetwork()
    net.add(DenseLayer(2, 3))
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(DenseLayer(3, 1))
    net.add(ActivationLayer(tanh, tanh_prime))

    
    net.set_loss(mse, mse_prime)
    net.train(x_train, y_train, epochs=1000, learning_rate=0.1)

    
    print("\nInference Results:")
    predictions = net.predict(x_train)
    for x, y in zip(x_train, predictions):
        print(f"Input: {x[0]} Predicted Output: {y[0]}")

def test_dense_layer_shapes():
    
    layer = DenseLayer(2, 3)
    input_data = np.array([[1, 2]])
    output = layer.forward(input_data)
    assert output.shape == (1, 3), f"Expected shape (1, 3), got {output.shape}"
    print("Unit Test Passed: DenseLayer shape is correct.")

if __name__ == "__main__":
    test_dense_layer_shapes()
    run_example()