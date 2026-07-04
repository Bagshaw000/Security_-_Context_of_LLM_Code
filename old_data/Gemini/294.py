from typing import List, Dict, Tuple

class ImageClassificationEnsemble:
    

    def __init__(self):
        pass

    def aggregate_predictions(self, predictions: List[Dict[str, float]]) -> Tuple[str, float]:
        
        if not predictions:
            raise ValueError("Prediction list must contain at least one model output.")

        num_models = len(predictions)
        aggregated_scores: Dict[str, float] = {}

        
        for model_output in predictions:
            for label, probability in model_output.items():
                aggregated_scores[label] = aggregated_scores.get(label, 0.0) + probability

        
        best_label = ""
        max_avg_confidence = -1.0

        for label, total_prob in aggregated_scores.items():
            avg_confidence = total_prob / num_models
            if avg_confidence > max_avg_confidence:
                max_avg_confidence = avg_confidence
                best_label = label

        return best_label, max_avg_confidence

def main():
    
    
    model_outputs = [
        {"Object_A": 0.85, "Object_B": 0.10, "Object_C": 0.05},
        {"Object_A": 0.70, "Object_B": 0.25, "Object_C": 0.05},
        {"Object_A": 0.40, "Object_B": 0.55, "Object_C": 0.05}
    ]

    ensemble = ImageClassificationEnsemble()
    final_class, confidence = ensemble.aggregate_predictions(model_outputs)

    print(f"Consensus Classification: {final_class}")
    print(f"Ensemble Confidence Level: {confidence:.4f}")

if __name__ == "__main__":
    main()