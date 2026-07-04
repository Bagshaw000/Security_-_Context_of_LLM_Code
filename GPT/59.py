def combine_classifications(classifications, confidences):
    from collections import Counter

    
    combined = Counter()
    for classification, confidence in zip(classifications, confidences):
        combined[classification] += confidence

    
    most_common_class, most_common_confidence = combined.most_common(1)[0]

    
    total_confidence = sum(combined.values())
    confidence_level = most_common_confidence / total_confidence

    return most_common_class, confidence_level


classifications = ['cat', 'dog', 'cat', 'cat', 'dog']
confidences = [0.8, 0.6, 0.9, 0.7, 0.5]
result = combine_classifications(classifications, confidences)
print(result)