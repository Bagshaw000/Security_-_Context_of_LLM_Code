import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255


model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),  
    layers.Dense(128, activation='relu'),   
    layers.Dense(10, activation='softmax')  
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


model.fit(x_train, y_train, epochs=5)


test_loss, test_acc = model.evaluate(x_test, y_test)


print(f'Test accuracy: {test_acc}')