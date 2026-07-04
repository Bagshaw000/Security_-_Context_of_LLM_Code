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
    
    
    total_confidence = 0
    for i, classification in enumerate(classifications):
        if classification == most_likely_classification:
            total_confidence += confidence_levels[i]
    confidence_level = total_confidence / max_count
    
    return most_likely_classification, confidence_level