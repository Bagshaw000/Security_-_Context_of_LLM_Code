import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import unittest


def create_model(input_shape, num_classes):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def train_model(model, x_train, y_train, epochs=10, batch_size=32):
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)


def evaluate_model(model, x_test, y_test):
    return model.evaluate(x_test, y_test)


class TestDeepNeuralNetwork(unittest.TestCase):
    def setUp(self):
        self.input_shape = (20,)
        self.num_classes = 3
        self.model = create_model(self.input_shape, self.num_classes)
        self.x_train = np.random.rand(100, 20)
        self.y_train = np.random.randint(0, 3, 100)
        self.x_test = np.random.rand(20, 20)
        self.y_test = np.random.randint(0, 3, 20)

    def test_model_creation(self):
        self.assertIsNotNone(self.model)

    def test_training(self):
        train_model(self.model, self.x_train, self.y_train)
        loss, accuracy = evaluate_model(self.model, self.x_test, self.y_test)
        self.assertIsInstance(loss, float)
        self.assertIsInstance(accuracy, float)

if __name__ == '__main__':
    unittest.main()