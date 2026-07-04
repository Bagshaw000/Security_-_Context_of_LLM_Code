import numpy as np

def combine_classifications(classifications, confidences):
    
    
    class_counts = {}
    for classification, confidence in zip(classifications, confidences):
        if classification in class_counts:
            class_counts[classification] += confidence
        else:
            class_counts[classification] = confidence

    
    most_likely_class = max(class_counts, key=class_counts.get)
    confidence_level = class_counts[most_likely_class] / sum(class_counts.values())

    return most_likely_class, confidence_level