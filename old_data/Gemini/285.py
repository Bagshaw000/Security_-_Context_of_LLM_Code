import numpy as np

def combine_model_predictions(predictions):
    
    if not predictions or not predictions[0]:
        raise ValueError("Predictions list cannot be empty.")

    
    
    preds_matrix = np.array(predictions)
    
    
    
    mean_probabilities = np.mean(preds_matrix, axis=0)
    
    
    best_class_index = int(np.argmax(mean_probabilities))
    
    
    confidence_score = float(mean_probabilities[best_class_index])
    
    return best_class_index, confidence_score

def test_aggregation_logic():
    
    
    model_1 = [0.10, 0.05, 0.70, 0.10, 0.05]
    model_2 = [0.20, 0.10, 0.60, 0.05, 0.05]
    model_3 = [0.05, 0.05, 0.80, 0.05, 0.05]
    
    ensemble_input = [model_1, model_2, model_3]
    
    class_idx, confidence = combine_model_predictions(ensemble_input)
    
    
    expected_class = 2
    expected_confidence = 0.7
    
    assert class_idx == expected_class, f"Expected {expected_class}, got {class_idx}"
    assert abs(confidence - expected_confidence) < 1e-6, "Confidence calculation mismatch"
    
    print(f"Consensus Classification: Class {class_idx}")
    print(f"Ensemble Confidence Level: {confidence:.4f}")

if __name__ == "__main__":
    
    try:
        test_aggregation_logic()
        print("Unit test passed successfully.")
    except Exception as e:
        print(f"Unit test failed: {e}")