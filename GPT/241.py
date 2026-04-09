import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def generate_data(num_samples):
    X = np.random.rand(num_samples, 10)
    y = (np.sum(X, axis=1) > 5).astype(int)
    return X, y


def create_model(input_shape):
    model = keras.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=input_shape))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model


def main():
    X, y = generate_data(1000)
    model = create_model((10,))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=10, batch_size=32)

if __name__ == "__main__":
    main()