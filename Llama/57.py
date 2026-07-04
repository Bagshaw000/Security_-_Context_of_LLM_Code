import numpy as np
from sklearn.metrics import confusion_matrix

def classify_image(image_path, neural_networks):
    classifications = []
    for network in neural_networks:
        prediction = network.predict(image_path)
        classification = np.argmax(prediction)
        confidence = np.max(prediction)
        classifications.append((classification, confidence))
    return classifications

def combine_classifications(classifications):
    predictions = [cls[0] for cls in classifications]
    confidences = [cls[1] for cls in classifications]

    
    best_index = np.argmax(confidences)

    
    top_classifications = [(cls, conf) for cls, conf in zip(predictions, confidences) if conf > 0.5]

    
    if len(top_classifications) > 1:
        best_classification = max(top_classifications, key=lambda x: x[1])
    else:
        best_classification = top_classifications[0]

    return best_classification

def main():
    
    networks = [load_network(), load_network()]

    
    image_path = 'path_to_your_image.jpg'

    classifications = classify_image(image_path, networks)
    combined_classification = combine_classifications(classifications)

    print(f"Combined classification: {combined_classification[0]} with confidence: {combined_classification[1]*100}%")

if __name__ == "__main__":
    main()