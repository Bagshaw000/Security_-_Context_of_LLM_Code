import collections

def aggregate_neural_network_predictions(predictions):
    
    if not predictions or not predictions[0]:
        return {"error": "No prediction data provided."}

    num_models = len(predictions)
    num_classes = len(predictions[0])

    
    combined_probabilities = [0.0] * num_classes

    
    for model_output in predictions:
        if len(model_output) != num_classes:
            raise ValueError("All models must have the same number of output classes.")
        for i in range(num_classes):
            combined_probabilities[i] += model_output[i]

    
    mean_probabilities = [p / num_models for p in combined_probabilities]

    
    max_confidence = max(mean_probabilities)
    predicted_class = mean_probabilities.index(max_confidence)

    return {
        "predicted_class": predicted_class,
        "confidence": round(max_confidence, 4)
    }

def run_unit_test():
    
    
    
    
    
    mock_predictions = [
        [0.1, 0.8, 0.1],
        [0.3, 0.4, 0.3],
        [0.6, 0.2, 0.2]
    ]
    
    
    
    
    
    result = aggregate_neural_network_predictions(mock_predictions)
    
    assert result["predicted_class"] == 1
    assert result["confidence"] == 0.4667
    print("Unit test passed: Logic correctly identified Class 1 as the ensemble winner.")

if __name__ == "__main__":
    
    
    model_results = [
        [0.02, 0.95, 0.03],
        [0.05, 0.90, 0.05],
        [0.10, 0.80, 0.10],
        [0.01, 0.98, 0.01]
    ]

    final_output = aggregate_neural_network_predictions(model_results)
    
    print(f"Ensemble Prediction Results:")
    print(f"Most Likely Classification: Class {final_output['predicted_class']}")
    print(f"Confidence Level: {final_output['confidence'] * 100}%")

    
    run_unit_test()