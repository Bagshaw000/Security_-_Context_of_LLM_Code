import collections
import unittest

def get_ensemble_prediction(classifications):
    
    if not classifications:
        return {"label": None, "confidence": 0.0}

    total_votes = len(classifications)
    counts = collections.Counter(classifications)
    
    
    most_common_label, vote_count = counts.most_common(1)[0]
    
    
    confidence = vote_count / total_votes
    
    return {
        "label": most_common_label,
        "confidence": confidence
    }

class TestEnsembleMethod(unittest.TestCase):
    def test_majority_success(self):
        data = ["A", "B", "A", "A", "C"]
        result = get_ensemble_prediction(data)
        self.assertEqual(result["label"], "A")
        self.assertEqual(result["confidence"], 0.6)

    def test_unanimous(self):
        data = ["Dog", "Dog", "Dog"]
        result = get_ensemble_prediction(data)
        self.assertEqual(result["label"], "Dog")
        self.assertEqual(result["confidence"], 1.0)

    def test_empty(self):
        result = get_ensemble_prediction([])
        self.assertIsNone(result["label"])
        self.assertEqual(result["confidence"], 0.0)

if __name__ == "__main__":
    
    model_outputs = [
        "golden_retriever", 
        "labrador", 
        "golden_retriever", 
        "golden_retriever", 
        "cocker_spaniel",
        "golden_retriever",
        "golden_retriever",
        "labrador"
    ]
    
    prediction_data = get_ensemble_prediction(model_outputs)
    
    print(f"Most Likely Classification: {prediction_data['label']}")
    print(f"Confidence Level: {prediction_data['confidence']:.2%}")
    
    
    print("\nStarting Unit Tests...")
    unittest.main(argv=[''], exit=False)