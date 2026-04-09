from collections import Counter

def combine_classifications(classifications, confidences):
    
    
    weighted_classifications = Counter()
    
    for classification, confidence in zip(classifications, confidences):
        weighted_classifications[classification] += confidence
    
    
    most_common_class, total_confidence = weighted_classifications.most_common(1)[0]
    
    
    confidence_level = total_confidence / sum(confidences)
    
    return most_common_class, confidence_level


classifications = ['cat', 'dog', 'cat', 'cat', 'dog']
confidences = [0.9, 0.6, 0.8, 0.95, 0.7]

result = combine_classifications(classifications, confidences)
print(result)  