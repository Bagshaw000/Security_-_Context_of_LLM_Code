






import tensorflow as tf
import numpy as np





input_numbers = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=float)
output_answers = np.array([2.0, 4.0, 6.0, 8.0, 10.0], dtype=float)





model = tf.keras.Sequential([
    
    tf.keras.layers.Dense(units=16, activation='relu', input_shape=[1]),
    
    tf.keras.layers.Dense(units=16, activation='relu'),
    
    tf.keras.layers.Dense(units=1)
])





model.compile(optimizer='adam', loss='mean_squared_error')




print("The neural network is currently learning the pattern...")
model.fit(input_numbers, output_answers, epochs=500, verbose=0)
print("Learning complete.")




new_number = np.array([10.0])
prediction = model.predict(new_number)

print("If the input is 10, the neural network predicts the result is:")
print(prediction)


