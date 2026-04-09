import numpy as np

def combine_classifications(classifications, confidences):
    
    
    weighted_avg = np.average(classifications, weights=confidences)
    
    
    most_likely_class = round(weighted_avg)
    
    
    overall_confidence = np.max(confidences)
    
    return most_likely_class, overall_confidence