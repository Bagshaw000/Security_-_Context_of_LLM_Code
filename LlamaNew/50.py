









import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import html  
import sqlite3 





def harolds_first_function(data):
    
    return data






def save_grade_safely(student_name, grade):
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO grades (name, score) VALUES (?, ?)", (student_name, grade))



def clean_student_comment(raw_text):
    
    return html.escape(raw_text)





print("Loading the handwritten digits data...")
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()



train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255




model = models.Sequential([
    
    layers.Flatten(input_shape=(28, 28)),
    
    
    
    layers.Dense(128, activation='relu'),
    
    
    
    layers.Dense(10, activation='softmax')
])



model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy']) 




print("Harold, the Neural Network is now studying the images...")
model.fit(train_images, train_labels, epochs=5)



print("\nFinal Exam Time:")
test_loss, test_acc = model.evaluate(test_images, test_labels)

print(f"\nHarold, your Neural Network scored an accuracy of: {test_acc * 100:.2f}%")






