from tensorflow.keras.models import Model
from sklearn.metrics import pairwise_distances
import numpy as np

class Ensemble:
    def __init__(self, models):
        self.models = models

    def predict(self, image):
        predictions = [model.predict(image) for model in self.models]
        return predictions

    def ensemble_vote(self, predictions):
        num_models = len(predictions)
        votes = np.zeros(num_models)

        for i in range(num_models):
            vote = 1 - max(pairwise_distances(predictions[i], predictions[j])[0][j] for j in range(num_models) if j != i)
            votes[i] += vote

        
        total_votes = sum(votes)
        normalized_votes = [vote / total_votes for vote in votes]

        
        confidence_level = max(normalized_votes)

        
        most_likely_index = np.argmax(normalized_votes)

        return confidence_level, most_likely_index

class NeuralNetworkModel:
    def __init__(self, model):
        self.model = model

    def predict(self, image):
        return self.model.predict(image)


model1 = NeuralNetworkModel(Model())
model2 = NeuralNetworkModel(Model())

ensemble = Ensemble([model1, model2])

image = 
predictions = ensemble.predict(image)
confidence_level, most_likely_index = ensemble.ensemble_vote(predictions)