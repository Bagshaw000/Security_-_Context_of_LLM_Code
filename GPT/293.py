from collections import Counter

def combine_classifications(classifications, confidences):
    
    
    weighted_counts = Counter()
    
    for classification, confidence in zip(classifications, confidences):
        weighted_counts[classification] += confidence

    
    most_common_class, total_confidence = weighted_counts.most_common(1)[0]
    
    
    confidence_level = total_confidence / sum(confidences) * 100
    
    return most_common_class, confidence_level


classifications = ['cat', 'dog', 'cat', 'cat', 'dog']
confidences = [0.8, 0.6, 0.9, 0.7, 0.5]
result = combine_classifications(classifications, confidences)
print(result)  