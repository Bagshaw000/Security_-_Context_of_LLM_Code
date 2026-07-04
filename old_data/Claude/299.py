import numpy as np

def combine_classifications(classifications, confidences):
    
    
    classification_counts = {}
    for i, classification in enumerate(classifications):
        if classification in classification_counts:
            classification_counts[classification] += confidences[i]
        else:
            classification_counts[classification] = confidences[i]
    
    
    max_classification = max(classification_counts, key=classification_counts.get)
    max_confidence = classification_counts[max_classification] / sum(classification_counts.values())
    
    return max_classification, max_confidence