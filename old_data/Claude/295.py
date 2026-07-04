import numpy as np

def combine_classifications(classifications, confidences):
    
    
    weighted_sum = sum([c * conf for c, conf in zip(classifications, confidences)])
    
    
    total_confidence = sum(confidences)
    
    
    final_classification = np.argmax(weighted_sum)
    final_confidence = weighted_sum[final_classification] / total_confidence
    
    return final_classification, final_confidence