import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def build_deep_neural_network(input_size, output_size, hidden_layers, dropout_rate=0.0):
    model = Sequential()
    model.add(Dense(hidden_layers[0], input_dim=input_size, activation='relu'))
    model.add(Dropout(dropout_rate))
    
    for layer_size in hidden_layers[1:]:
        model.add(Dense(layer_size, activation='relu'))
        model.add(Dropout(dropout_rate))
    
    model.add(Dense(output_size, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model


input_size = 100
output_size = 10
hidden_layers = [64, 32, 16]
dropout_rate = 0.2

model = build_deep_neural_network(input_size, output_size, hidden_layers, dropout_rate)
print(model.summary())