import numpy as np

def combine_classifications(classifications, confidences):
    
    
    classification_counts = {}
    for i, classification in enumerate(classifications):
        if classification not in classification_counts:
            classification_counts[classification] = 0
        classification_counts[classification] += confidences[i]

    
    most_likely_classification = max(classification_counts, key=classification_counts.get)
    confidence_level = classification_counts[most_likely_classification] / sum(classification_counts.values())

    return most_likely_classification, confidence_level