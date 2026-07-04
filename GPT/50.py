import numpy as np
import tensorflow as tf
from tensorflow import keras


X_train = np.random.rand(1000, 10)
y_train = np.random.randint(2, size=(1000, 1))


model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(10,)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=10, batch_size=32)


X_test = np.random.rand(100, 10)
y_test = np.random.randint(2, size=(100, 1))


test_loss, test_accuracy = model.evaluate(X_test, y_test)
print('Test accuracy:', test_accuracy)