import numpy as np

def combine_neural_network_outputs(model_predictions):
    
    
    predictions_matrix = np.array(model_predictions)
    
    
    
    mean_probabilities = np.mean(predictions_matrix, axis=0)
    
    
    winning_class = np.argmax(mean_probabilities)
    
    
    confidence_level = mean_probabilities[winning_class]
    
    return int(winning_class), float(confidence_level)

def run_ensemble_example():
    
    
    
    model_1_output = [0.10, 0.85, 0.05]
    model_2_output = [0.20, 0.70, 0.10]
    model_3_output = [0.05, 0.90, 0.05]
    model_4_output = [0.40, 0.30, 0.30] 
    
    all_outputs = [model_1_output, model_2_output, model_3_output, model_4_output]
    
    class_idx, confidence = combine_neural_network_outputs(all_outputs)
    
    class_mapping = {0: "Cat", 1: "Dog", 2: "Bird"}
    
    print(f"Input model predictions collected: {len(all_outputs)}")
    print(f"Resulting Classification: {class_mapping[class_idx]}")
    print(f"Ensemble Confidence Level: {confidence:.4f}")

if __name__ == "__main__":
    
    run_ensemble_example()