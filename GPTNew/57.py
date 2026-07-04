import numpy as np
from collections import Counter

class ImageClassifier:
    def __init__(self, models):
        self.models = models

    def classify_image(self, image):
        predictions = []
        confidences = []

        for model in self.models:
            try:
                prediction, confidence = model.predict(image)
                predictions.append(prediction)
                confidences.append(confidence)
            except Exception as e:
                print(f"Error in model {model}: {e}")

        return self.combine_predictions(predictions, confidences)

    def combine_predictions(self, predictions, confidences):
        if not predictions:
            return None, 0

        
        prediction_counts = Counter(predictions)
        most_common_prediction, count = prediction_counts.most_common(1)[0]
        
        
        total_confidence = sum(confidences[i] for i in range(len(predictions)) if predictions[i] == most_common_prediction)
        confidence_level = total_confidence / count if count > 0 else 0

        return most_common_prediction, confidence_level


class DummyModel:
    def predict(self, image):
        
        return np.random.choice(['cat', 'dog', 'bird']), np.random.random()

models = [DummyModel() for _ in range(5)]
classifier = ImageClassifier(models)

image = "path/to/image.jpg"  
final_prediction, confidence = classifier.classify_image(image)
print(f"Final Prediction: {final_prediction}, Confidence: {confidence:.2f}")