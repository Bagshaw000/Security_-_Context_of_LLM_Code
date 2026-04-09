import numpy as np
from typing import List, Tuple, Union

class ImageClassificationAggregator:
    

    def __init__(self, num_classes: int):
        
        self.num_classes = num_classes

    def aggregate_predictions(self, predictions: List[Union[List[float], np.ndarray]]) -> Tuple[int, float]:
        
        if not predictions:
            raise ValueError("The list of classifications cannot be empty.")

        
        preds_array = np.array(predictions)

        
        if preds_array.ndim != 2 or preds_array.shape[1] != self.num_classes:
            raise ValueError(f"Each model must provide a probability vector of size {self.num_classes}")

        
        
        
        mean_probabilities = np.mean(preds_array, axis=0)

        
        predicted_class_index = int(np.argmax(mean_probabilities))
        confidence_level = float(mean_probabilities[predicted_class_index])

        return predicted_class_index, confidence_level

def main():
    
    
    model_outputs = [
        [0.05, 0.85, 0.05, 0.05],  
        [0.10, 0.70, 0.10, 0.10],  
        [0.20, 0.40, 0.30, 0.10]   
    ]

    
    aggregator = ImageClassificationAggregator(num_classes=4)

    try:
        
        best_class, confidence = aggregator.aggregate_predictions(model_outputs)

        
        print(f"Aggregated Classification Result: Class {best_class}")
        print(f"System-wide Confidence Level: {confidence:.4%}")
        
    except Exception as e:
        print(f"Error during aggregation: {e}")

if __name__ == "__main__":
    main()