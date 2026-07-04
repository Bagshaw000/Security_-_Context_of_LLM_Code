
import numpy as np

def combine_classifications(classifications):
    
    probabilities = np.array([cls[1] for cls in classifications])
    
    
    max_idx = np.argmax(probabilities)
    second_max_idx = np.argsort(-probabilities, axis=0)[0][-2]
    
    
    confidence_level = (probabilities[max_idx] - probabilities[second_max_idx]) / (probabilities[max_idx] + probabilities[second_max_idx])
    
    return max_idx, probability_to_class(max_idx), confidence_level

def probability_to_class(index):
    classes = ['class_1', 'class_2', 'class_3']  
    return classes[index]


classifications = [
    [0.8, 'class_1'], 
    [0.3, 'class_2'], 
    [0.05, 'class_3']
]
index, prediction, confidence_level = combine_classifications(classifications)
print(f'Predicted class: {prediction}, Confidence level: {confidence_level:.2f}')
