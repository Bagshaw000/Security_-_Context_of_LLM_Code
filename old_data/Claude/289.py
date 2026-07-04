import numpy as np

def combine_classifications(classifications, confidences):
    num_networks = len(classifications)
    class_counts = {}
    for i in range(num_networks):
        classification = classifications[i]
        confidence = confidences[i]
        if classification in class_counts:
            class_counts[classification] += confidence
        else:
            class_counts[classification] = confidence
    
    sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
    most_likely_class = sorted_classes[0][0]
    confidence_level = sorted_classes[0][1] / sum(class_counts.values())
    
    return most_likely_class, confidence_level