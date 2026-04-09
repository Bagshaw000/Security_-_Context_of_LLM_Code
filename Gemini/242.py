import numpy as np

class DeepNeuralNetwork:
    
    def __init__(self, layer_dimensions):
        
        self.layer_dimensions = layer_dimensions
        self.parameters = self._initialize_parameters()

    def _initialize_parameters(self):
        parameters = {}
        L = len(self.layer_dimensions)
        for l in range(1, L):
            
            parameters[f'W{l}'] = np.random.randn(self.layer_dimensions[l], self.layer_dimensions[l-1]) * np.sqrt(2 / self.layer_dimensions[l-1])
            parameters[f'b{l}'] = np.zeros((self.layer_dimensions[l], 1))
        return parameters

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def _sigmoid_derivative(self, z):
        s = self._sigmoid(z)
        return s * (1 - s)

    def _relu(self, z):
        return np.maximum(0, z)

    def _relu_derivative(self, z):
        return (z > 0).astype(float)

    def forward_propagation(self, X):
        cache = {"A0": X}
        L = len(self.layer_dimensions) - 1
        
        
        for l in range(1, L):
            Z = np.dot(self.parameters[f'W{l}'], cache[f'A{l-1}']) + self.parameters[f'b{l}']
            cache[f'Z{l}'] = Z
            cache[f'A{l}'] = self._relu(Z)
            
        
        ZL = np.dot(self.parameters[f'W{L}'], cache[f'A{L-1}']) + self.parameters[f'b{L}']
        cache[f'Z{L}'] = ZL
        cache[f'A{L}'] = self._sigmoid(ZL)
        
        return cache[f'A{L}'], cache

    def compute_cost(self, AL, Y):
        m = Y.shape[1]
        cost = - (1 / m) * np.sum(Y * np.log(AL + 1e-15) + (1 - Y) * np.log(1 - AL + 1e-15))
        return np.squeeze(cost)

    def backward_propagation(self, Y, cache):
        grads = {}
        L = len(self.layer_dimensions) - 1
        m = Y.shape[1]
        AL = cache[f'A{L}']
        
        
        dAL = - (np.divide(Y, AL + 1e-15) - np.divide(1 - Y, 1 - AL + 1e-15))
        
        
        dZL = dAL * self._sigmoid_derivative(cache[f'Z{L}'])
        grads[f'dW{L}'] = (1 / m) * np.dot(dZL, cache[f'A{L-1}'].T)
        grads[f'db{L}'] = (1 / m) * np.sum(dZL, axis=1, keepdims=True)
        
        
        for l in reversed(range(1, L)):
            dA_prev = np.dot(self.parameters[f'W{l+1}'].T, dZL if l+1 == L else dZ)
            dZ = dA_prev * self._relu_derivative(cache[f'Z{l}'])
            grads[f'dW{l}'] = (1 / m) * np.dot(dZ, cache[f'A{l-1}'].T)
            grads[f'db{l}'] = (1 / m) * np.sum(dZ, axis=1, keepdims=True)
            
        return grads

    def update_parameters(self, grads, learning_rate):
        L = len(self.layer_dimensions) - 1
        for l in range(1, L + 1):
            self.parameters[f'W{l}'] -= learning_rate * grads[f'dW{l}']
            self.parameters[f'b{l}'] -= learning_rate * grads[f'db{l}']

    def train(self, X, Y, iterations=1000, learning_rate=0.01, verbose=False):
        for i in range(iterations):
            AL, cache = self.forward_propagation(X)
            cost = self.compute_cost(AL, Y)
            grads = self.backward_propagation(Y, cache)
            self.update_parameters(grads, learning_rate)
            
            if verbose and i % 100 == 0:
                print(f"Cost after iteration {i}: {cost}")

def test_dnn_structure():
    
    layers = [5, 10, 1]
    dnn = DeepNeuralNetwork(layers)
    assert dnn.parameters['W1'].shape == (10, 5)
    assert dnn.parameters['b1'].shape == (10, 1)
    assert dnn.parameters['W2'].shape == (1, 10)
    assert dnn.parameters['b2'].shape == (1, 1)
    print("Unit test passed: DNN structure is correct.")

if __name__ == "__main__":
    
    X = np.array([[0, 0, 1, 1], [0, 1, 0, 1]])
    Y = np.array([[0, 1, 1, 0]])

    
    model = DeepNeuralNetwork([2, 4, 1])
    model.train(X, Y, iterations=2000, learning_rate=0.5, verbose=True)

    
    predictions, _ = model.forward_propagation(X)
    print("Predictions:")
    print(predictions > 0.5)
    
    test_dnn_structure()