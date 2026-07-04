import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def create_model(input_shape, num_classes):
    model = keras.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(num_classes, activation='softmax'))
    return model


def compile_model(model):
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])


def train_model(model, x_train, y_train, epochs=10, batch_size=32):
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)


if __name__ == "__main__":
    
    x_train = np.random.random((1000, 20))
    y_train = np.random.randint(10, size=(1000,))

    
    model = create_model(input_shape=(20,), num_classes=10)
    compile_model(model)

    
    train_model(model, x_train, y_train)