import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.optimizers import Adam

class DeepNeuralNetwork:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=self.input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, kernel_size=3, activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        return model

    def compile_model(self, learning_rate):
        optimizer = Adam(lr=learning_rate)
        model = self.build_model()
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    def train_model(self, X_train, y_train, X_test, y_test, epochs):
        model = self.build_model()
        model = self.compile_model(learning_rate=0.001)
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs)
        return history


input_shape = (28, 28, 1)
num_classes = 10
X_train, X_test, y_train, y_test = np.random.rand(1000, 28, 28, 1), np.random.rand(1000, 28, 28, 1), np.random.randint(0, 10, 1000), np.random.randint(0, 10, 1000)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train).reshape(-1, 28*28)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

nn = DeepNeuralNetwork(input_shape=input_shape, num_classes=num_classes)
history = nn.train_model(X_train, y_train, X_test, y_test, epochs=10)