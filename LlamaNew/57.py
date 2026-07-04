import collections
from typing import List, Dict, Tuple

class ClassificationAggregator:
    

    @staticmethod
    def validate_input(predictions: List[Dict[str, float]]) -> None:
        
        if not isinstance(predictions, list):
            raise TypeError("Input 'predictions' must be a list of dictionaries.")
        
        if not predictions:
            raise ValueError("Input 'predictions' list cannot be empty.")

        for idx, model_output in enumerate(predictions):
            if not isinstance(model_output, dict):
                raise TypeError(f"Output at index {idx} must be a dictionary.")
            
            for label, score in model_output.items():
                if not isinstance(label, str):
                    raise TypeError(f"Label '{label}' in model {idx} must be a string.")
                if not isinstance(score, (int, float)):
                    raise TypeError(f"Confidence score for '{label}' in model {idx} must be numeric.")
                if not (0.0 <= score <= 1.0):
                    raise ValueError(f"Confidence score for '{label}' in model {idx} must be between 0.0 and 1.0.")

    @classmethod
    def get_aggregated_classification(cls, predictions: List[Dict[str, float]]) -> Tuple[str, float]:
        
        
        cls.validate_input(predictions)

        num_models = len(predictions)
        score_accumulator = collections.defaultdict(float)

        
        for model_output in predictions:
            for label, score in model_output.items():
                score_accumulator[label] += float(score)

        if not score_accumulator:
            raise ValueError("No valid labels found in the provided network outputs.")

        
        
        final_results = {
            label: total_score / num_models 
            for label, total_score in score_accumulator.items()
        }

        
        winning_label = max(final_results, key=final_results.get)
        
        return winning_label, final_results[winning_label]

def run_unit_test():
    
    aggregator = ClassificationAggregator()
    
    
    mock_outputs = [
        {"cat": 0.85, "dog": 0.10, "bird": 0.05},
        {"cat": 0.70, "dog": 0.20, "bird": 0.10},
        {"cat": 0.90, "dog": 0.05, "bird": 0.05}
    ]
    
    try:
        label, confidence = aggregator.get_aggregated_classification(mock_outputs)
        print(f"Test Passed - Label: {label}, Confidence: {confidence:.4f}")
        
        
        malicious_input = [{"cat": 1.5}]
        aggregator.get_aggregated_classification(malicious_input)
    except ValueError as e:
        print(f"Security Validation Caught Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    run_unit_test()