import numpy as np

def combine_classifications(classifications, confidence_thresholds):
    
    
    vote_counts = {}
    for classification in classifications:
        if classification in vote_counts:
            vote_counts[classification] += 1
        else:
            vote_counts[classification] = 1
    
    
    max_votes = 0
    most_likely_classification = None
    for classification, count in vote_counts.items():
        if count > max_votes:
            max_votes = count
            most_likely_classification = classification
    
    
    total_votes = sum(vote_counts.values())
    confidence_level = max_votes / total_votes
    
    
    for i, threshold in enumerate(confidence_thresholds):
        if confidence_level >= threshold:
            return most_likely_classification, confidence_level
    
    
    return most_likely_classification, 0.0