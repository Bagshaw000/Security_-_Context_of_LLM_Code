import numpy as np

class ImageClassificationAggregator:
    
    def __init__(self, class_labels):
        self.class_labels = class_labels

    def combine_predictions(self, model_outputs):
        
        if not model_outputs:
            raise ValueError("The list of model outputs cannot be empty.")

        
        predictions_matrix = np.array(model_outputs)
        
        
        
        mean_probabilities = np.mean(predictions_matrix, axis=0)
        
        
        max_index = np.argmax(mean_probabilities)
        
        predicted_label = self.class_labels[max_index]
        confidence_level = mean_probabilities[max_index]
        
        return predicted_label, float(confidence_level)

def main():
    
    labels = ["Airplane", "Automobile", "Bird", "Cat", "Deer"]
    
    
    
    network_1_probs = [0.05, 0.05, 0.10, 0.70, 0.10]
    network_2_probs = [0.02, 0.08, 0.05, 0.80, 0.05]
    network_3_probs = [0.10, 0.10, 0.20, 0.50, 0.10]
    
    all_network_data = [network_1_probs, network_2_probs, network_3_probs]
    
    
    aggregator = ImageClassificationAggregator(labels)
    
    
    final_guess, confidence = aggregator.combine_predictions(all_network_data)
    
    print(f"Consensus Prediction: {final_guess}")
    print(f"Confidence Level: {confidence:.4f}")

if __name__ == "__main__":
    main()