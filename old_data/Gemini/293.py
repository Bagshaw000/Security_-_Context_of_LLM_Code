from typing import List, Dict, Tuple
from collections import defaultdict

class NeuralConsensusEngine:
    

    def __init__(self, model_outputs: List[Dict[str, float]]):
        
        self.model_outputs = model_outputs

    def aggregate_consensus(self) -> Tuple[str, float]:
        
        if not self.model_outputs:
            raise ValueError("No model outputs available for aggregation.")

        n = len(self.model_outputs)
        aggregated_probabilities = defaultdict(float)

        
        for prediction_set in self.model_outputs:
            for label, score in prediction_set.items():
                aggregated_probabilities[label] += score

        
        mean_probabilities = {
            label: total_score / n 
            for label, total_score in aggregated_probabilities.items()
        }

        
        winning_label = max(mean_probabilities, key=mean_probabilities.get)
        confidence_level = mean_probabilities[winning_label]

        return winning_label, confidence_level

def main():
    
    
    network_results = [
        {"Passkey": 0.92, "LegacyToken": 0.05, "Biometric": 0.03},
        {"Passkey": 0.85, "LegacyToken": 0.10, "Biometric": 0.05},
        {"Passkey": 0.40, "LegacyToken": 0.55, "Biometric": 0.05},
        {"Passkey": 0.95, "LegacyToken": 0.02, "Biometric": 0.03}
    ]

    engine = NeuralConsensusEngine(network_results)
    label, confidence = engine.aggregate_consensus()

    print(f"Consensus Classification: {label}")
    print(f"Aggregate Confidence Level: {confidence:.4%}")

if __name__ == "__main__":
    main()