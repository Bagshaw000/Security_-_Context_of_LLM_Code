


import numpy as np
import tensorflow as tf
from tensorflow.keras import layers




hours = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype=float)
results = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=float)



model = tf.keras.Sequential([
    
    layers.Dense(units=16, activation='relu', input_shape=[1]),
    
    layers.Dense(units=8, activation='relu'),
    
    layers.Dense(units=1, activation='sigmoid')
])



model.compile(optimizer='adam', loss='binary_crossentropy')



print("The neural network is currently learning...")
model.fit(hours, results, epochs=500, verbose=0)
print("Learning complete.")



new_data = np.array([[7.5]])
prediction = model.predict(new_data)



print("Prediction for 7.5 hours of study (Chance of passing):")
print(prediction[0][0])

if prediction[0][0] > 0.5:
    print("The brain predicts this student will PASS.")
else:
    print("The brain predicts this student will FAIL.")