import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split


X = np.array([ [ 0.1, 0.2 ], [ 0.3, 0.4 ], [ 0.5, 0.6 ], [ 0.7, 0.8 ] ])
y = np.array([ 0 , 1 , 1 , 0 ])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=10)


test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_acc}')