from collections import Counter

class ImageClassifier:
    def __init__(self, classifiers):
        self.classifiers = classifiers

    def classify(self, image):
        results = []
        for classifier in self.classifiers:
            label, confidence = classifier.predict(image)
            results.append((label, confidence))
        return self.combine_results(results)

    def combine_results(self, results):
        labels = [result[0] for result in results]
        confidences = [result[1] for result in results]
        
        
        label_count = Counter(labels)
        most_common_label, count = label_count.most_common(1)[0]
        
        
        total_confidence = sum(conf for label, conf in results if label == most_common_label)
        average_confidence = total_confidence / count
        
        return most_common_label, average_confidence





