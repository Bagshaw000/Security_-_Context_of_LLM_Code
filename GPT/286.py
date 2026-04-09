from collections import Counter

def combine_classifications(classifications, confidences):
    
    
    weighted_classifications = []
    for classification, confidence in zip(classifications, confidences):
        weighted_classifications.extend([classification] * int(confidence * 100))  

    
    classification_count = Counter(weighted_classifications)
    
    
    most_common_class, count = classification_count.most_common(1)[0]
    
    
    total_count = sum(classification_count.values())
    confidence_level = count / total_count

    return most_common_class, confidence_level


classifications = ['cat', 'dog', 'cat', 'cat', 'dog']
confidences = [0.8, 0.6, 0.9, 0.7, 0.5]
result = combine_classifications(classifications, confidences)
print(result)  