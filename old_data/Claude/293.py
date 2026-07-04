import numpy as np

def combine_classifications(classifications, confidences):
    
    
    class_counts = {}
    for i, classification in enumerate(classifications):
        if classification in class_counts:
            class_counts[classification] += confidences[i]
        else:
            class_counts[classification] = confidences[i]
    
    
    most_likely_class = max(class_counts, key=class_counts.get)
    total_confidence = class_counts[most_likely_class]
    confidence_level = total_confidence / sum(confidences)
    
    return most_likely_class, confidence_level