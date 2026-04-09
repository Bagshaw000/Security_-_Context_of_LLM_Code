





import numpy as np
import tensorflow as tf
from tensorflow.keras import layers





hours_studied = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype=float)
test_scores = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0], dtype=float)





model = tf.keras.Sequential([
    layers.Dense(units=4, input_shape=[1]), 
    layers.Dense(units=4),                  
    layers.Dense(units=1)                   
])




model.compile(optimizer='adam', loss='mean_squared_error')




print("The neural network is now learning the relationship between study hours and scores...")
model.fit(hours_studied, test_scores, epochs=500, verbose=0)
print("Learning complete.")





prediction = model.predict([10.0])

print("For 10 hours of study, the digital brain predicts a score of:")
print(prediction)

