import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam


input_dim = 100
output_dim = 10


model = Sequential()
model.add(Dense(64, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(output_dim, activation='softmax'))


model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])


X_train = np.random.rand(1000, input_dim)
y_train = np.random.randint(0, output_dim, (1000, output_dim))
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)