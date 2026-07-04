import numpy as np

class ClassificationEnsembleManager:
    
    
    def __init__(self):
        self.predictions = []

    def add_model_output(self, probability_distribution):
        
        self.predictions.append(np.array(probability_distribution))

    def compute_consensus(self):
        
        if not self.predictions:
            raise ValueError("No model outputs collected. Cannot compute consensus.")

        
        preds_matrix = np.vstack(self.predictions)
        
        
        
        mean_probabilities = np.mean(preds_matrix, axis=0)
        
        
        predicted_class = np.argmax(mean_probabilities)
        confidence_level = mean_probabilities[predicted_class]
        
        return {
            "predicted_class_index": int(predicted_class),
            "confidence_level": float(confidence_level)
        }

def run_ensemble_demo():
    
    
    
    
    
    network_results = [
        [0.05, 0.85, 0.05, 0.05],
        [0.10, 0.70, 0.10, 0.10],
        [0.20, 0.50, 0.20, 0.10]
    ]
    
    manager = ClassificationEnsembleManager()
    
    for result in network_results:
        manager.add_model_output(result)
        
    try:
        consensus = manager.compute_consensus()
        print(f"Aggregated Prediction: Class {consensus['predicted_class_index']}")
        print(f"System Confidence Level: {consensus['confidence_level']:.4f}")
    except Exception as e:
        print(f"Error in aggregation logic: {e}")

if __name__ == "__main__":
    run_ensemble_demo()