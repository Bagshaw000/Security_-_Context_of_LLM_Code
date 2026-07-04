







import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense





hours_studied = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
test_scores = np.array([45, 50, 55, 60, 65, 70, 75, 80, 85, 90], dtype=float)





model = Sequential([
    
    Dense(units=10, activation='relu', input_shape=[1]),
    
    
    
    Dense(units=5, activation='relu'),
    
    
    Dense(units=1)
])




model.compile(optimizer='adam', loss='mean_squared_error')




print("Harold, the computer is currently 'studying' the data...")
model.fit(hours_studied, test_scores, epochs=500, verbose=0)
print("The computer has finished learning!\n")




new_hours = np.array([12.0])
prediction = model.predict(new_hours)


print(f"For {new_hours[0]} hours of study, the predicted score is: {prediction[0][0]:.2f}")





