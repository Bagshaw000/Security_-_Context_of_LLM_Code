from collections import Counter

def combine_classifications(classifications, confidences):
    
    weighted_votes = Counter()
    
    for classification, confidence in zip(classifications, confidences):
        weighted_votes[classification] += confidence

    most_common_class, highest_confidence = weighted_votes.most_common(1)[0]
    
    return most_common_class, highest_confidence / sum(confidences)


classifications = ['cat', 'dog', 'cat', 'cat', 'dog']
confidences = [0.9, 0.6, 0.8, 0.95, 0.7]

result = combine_classifications(classifications, confidences)
print(result)  