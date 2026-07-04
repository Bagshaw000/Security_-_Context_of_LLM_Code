import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation


input_size = 100
output_size = 50


model = Sequential()
model.add(Dense(256, input_dim=input_size, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(output_size, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


X_train = np.random.rand(1000, input_size)
y_train = np.random.rand(1000, output_size)
model.fit(X_train, y_train, epochs=100, batch_size=32)


X_test = np.random.rand(100, input_size)
y_test = np.random.rand(100, output_size)
loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)