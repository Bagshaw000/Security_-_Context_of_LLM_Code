import numpy as np

def combine_classifications(classifications, confidences):
    
    
    class_counts = {}
    for i, c in enumerate(classifications):
        if c in class_counts:
            class_counts[c] += confidences[i]
        else:
            class_counts[c] = confidences[i]
    
    
    max_class = max(class_counts, key=class_counts.get)
    max_confidence = class_counts[max_class] / sum(class_counts.values())
    
    return max_class, max_confidence