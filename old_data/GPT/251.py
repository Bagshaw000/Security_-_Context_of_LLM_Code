import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


X_train = np.random.rand(1000, 20)
y_train = np.random.randint(2, size=(1000, 1))


model = keras.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(20,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=10, batch_size=32)


loss, accuracy = model.evaluate(X_train, y_train)
print(f'Loss: {loss}, Accuracy: {accuracy}')