from collections import Counter

def combine_classifications(classifications, confidences):
    
    weighted_votes = Counter()
    
    for classification, confidence in zip(classifications, confidences):
        weighted_votes[classification] += confidence

    most_common_class, total_confidence = weighted_votes.most_common(1)[0]
    confidence_level = total_confidence / sum(confidences)

    return most_common_class, confidence_level





