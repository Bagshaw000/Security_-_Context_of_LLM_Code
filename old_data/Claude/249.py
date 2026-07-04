import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import Adam


model = Sequential()
model.add(Dense(128, input_dim=64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])


X_train = np.random.rand(1000, 64)
y_train = np.random.randint(2, size=(1000, 1))
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)


X_test = np.random.rand(100, 64)
y_test = np.random.randint(2, size=(100, 1))
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')