import numpy as np

def combine_classifications(classifications, confidence_levels):
    
    
    classification_counts = {}
    for classification in classifications:
        if classification in classification_counts:
            classification_counts[classification] += 1
        else:
            classification_counts[classification] = 1
    
    
    max_count = 0
    most_likely_classification = None
    for classification, count in classification_counts.items():
        if count > max_count:
            max_count = count
            most_likely_classification = classification
    
    
    total_confidence = sum(confidence_levels)
    confidence_level = sum([confidence_levels[i] for i in range(len(classifications)) if classifications[i] == most_likely_classification]) / total_confidence
    
    return most_likely_classification, confidence_level