Here is the Python code for the task you described:

import numpy as np

def combine_classifications(classifications, confidences):
    
    
    class_counts = {}
    for c, conf in zip(classifications, confidences):
        if c in class_counts:
            class_counts[c] += conf
        else:
            class_counts[c] = conf
    
    
    most_likely_class = max(class_counts, key=class_counts.get)
    confidence = class_counts[most_likely_class] / sum(class_counts.values())
    
    return most_likely_class, confidence