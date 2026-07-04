import numpy as np

def combine_classifications(classifications, confidences):
    
    
    class_votes = {}
    for i, classification in enumerate(classifications):
        if classification not in class_votes:
            class_votes[classification] = 0
        class_votes[classification] += confidences[i]

    
    most_likely_class = max(class_votes, key=class_votes.get)
    confidence_level = class_votes[most_likely_class] / sum(confidences)

    return most_likely_class, confidence_level