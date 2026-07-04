



import tensorflow as tf
import numpy as np






inputs  = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=float)
results = np.array([12.0, 14.0, 16.0, 18.0, 20.0], dtype=float)




model = tf.keras.Sequential([
    
    tf.keras.layers.Dense(units=10, input_shape=[1]),
    
    tf.keras.layers.Dense(units=10),
    
    tf.keras.layers.Dense(units=5),
    
    tf.keras.layers.Dense(units=1)
])





model.compile(optimizer='adam', loss='mean_squared_error')




print("The computer is studying the data to find the hidden formula...")
model.fit(inputs, results, epochs=500, verbose=0)
print("The computer has finished learning!")




test_number = np.array([10.0])
prediction = model.predict(test_number)

print("If the input is 10, the computer predicts the result is:")
print(prediction[0][0])


