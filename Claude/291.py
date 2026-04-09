import numpy as np

def combine_classifications(classifications, confidences):
    
    
    class_counts = {}
    for i, classification in enumerate(classifications):
        if classification not in class_counts:
            class_counts[classification] = 0
        class_counts[classification] += confidences[i]
    
    
    max_count = 0
    max_class = None
    for classification, count in class_counts.items():
        if count > max_count:
            max_count = count
            max_class = classification
    
    
    total_confidence = sum(confidences)
    confidence_level = max_count / total_confidence
    
    return max_class, confidence_level