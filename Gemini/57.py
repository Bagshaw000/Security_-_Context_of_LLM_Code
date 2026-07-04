import numpy as np
from typing import List, Tuple

def get_ensemble_classification(model_outputs: List[List[float]]) -> Tuple[int, float]:
    
    
    
    predictions_matrix = np.array(model_outputs)
    
    
    
    average_probabilities = np.mean(predictions_matrix, axis=0)
    
    
    predicted_class = int(np.argmax(average_probabilities))
    
    
    confidence_level = float(average_probabilities[predicted_class])
    
    return predicted_class, confidence_level

def run_inventory_classification_ensemble():
    """
    Simulates the collection of classifications from n networks for an image
    and outputs the final decision based on the ensemble