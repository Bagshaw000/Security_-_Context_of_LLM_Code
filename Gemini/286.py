def combine_classifications(predictions):
    
    if not predictions or not predictions[0]:
        return None, 0.0
        
    num_models = len(predictions)
    num_classes = len(predictions[0])
    
    
    
    avg_probs = []
    for class_idx in range(num_classes):
        total_prob = sum(model_output[class_idx] for model_output in predictions)
        avg_probs.append(total_prob / num_models)
        
    
    max_confidence = max(avg_probs)
    best_class = avg_probs.index(max_confidence)
    
    return best_class, max_confidence

def collect_predictions(models, image_data):
    
    collected_outputs = []
    for model in models:
        
        prediction = model.predict(image_data)
        collected_outputs.append(prediction)
    return collected_outputs


if __name__ == "__main__":
    
    class MockNeuralNetwork:
        def __init__(self, mock_output):
            self.mock_output = mock_output
        def predict(self, data):
            return self.mock_output

    
    
    models = [
        MockNeuralNetwork([0.85, 0.10, 0.05]),
        MockNeuralNetwork([0.70, 0.20, 0.10]),
        MockNeuralNetwork([0.40, 0.50, 0.10])
    ]
    
    
    image_input = "binary_image_data_placeholder"
    
    
    individual_guesses = collect_predictions(models, image_input)
    
    
    predicted_index, confidence_score = combine_classifications(individual_guesses)
    
    
    class_map = {0: "Inventory Item A", 1: "Inventory Item B", 2: "Unknown"}
    print(f"Most Likely Classification: {class_map[predicted_index]}")
    print(f"Confidence Level: {confidence_score:.2%}")