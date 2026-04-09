import numpy as np

class EnsembleClassifier:
    

    def __init__(self, predictions):
        
        self.predictions = predictions

    def aggregate(self):
        
        if not self.predictions:
            return None, 0.0

        
        all_labels = set().union(*(p.keys() for p in self.predictions))
        num_models = len(self.predictions)
        
        
        summed_probabilities = {label: 0.0 for label in all_labels}

        
        for pred in self.predictions:
            for label, probability in pred.items():
                summed_probabilities[label] += probability

        
        best_label = None
        max_confidence = -1.0

        for label in summed_probabilities:
            
            average_prob = summed_probabilities[label] / num_models
            if average_prob > max_confidence:
                max_confidence = average_prob
                best_label = label

        return best_label, max_confidence

def run_ensemble_example():
    
    
    network_outputs = [
        {"Passkey": 0.88, "OTP": 0.08, "Password": 0.04},
        {"Passkey": 0.75, "OTP": 0.15, "Password": 0.10},
        {"Passkey": 0.92, "OTP": 0.05, "Password": 0.03},
        {"Passkey": 0.40, "OTP": 0.55, "Password": 0.05}
    ]

    ensemble = EnsembleClassifier(network_outputs)
    most_likely_class, confidence = ensemble.aggregate()

    print(f"Final Classification: {most_likely_class}")
    print(f"Confidence Level: {confidence:.2%}")

if __name__ == "__main__":
    run_ensemble_example()