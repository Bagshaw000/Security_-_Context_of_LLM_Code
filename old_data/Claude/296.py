import numpy as np

def combine_classifications(classifications, confidence_thresholds):
    
    
    
    combined_classifications = {}
    for classification in classifications:
        for label, confidence in classification.items():
            if label in combined_classifications:
                combined_classifications[label] += confidence
            else:
                combined_classifications[label] = confidence
    
    
    most_likely_label = max(combined_classifications, key=combined_classifications.get)
    total_confidence = sum(combined_classifications.values())
    confidence_level = combined_classifications[most_likely_label] / total_confidence
    
    
    if confidence_level >= min(confidence_thresholds):
        return most_likely_label, confidence_level
    else:
        return None, 0.0