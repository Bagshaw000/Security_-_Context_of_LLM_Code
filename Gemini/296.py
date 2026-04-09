import collections




neural_network_guesses = ["Golden Retriever", "Golden Retriever", "Labrador", "Golden Retriever", "Cocker Spaniel"]

def find_most_likely_classification(guesses):
    
    counts = collections.Counter(guesses)
    
    
    
    most_frequent_name, occurrences = counts.most_common(1)[0]
    
    
    
    total_guesses = len(guesses)
    confidence_percentage = (occurrences / total_guesses) * 100
    
    return most_frequent_name, confidence_percentage


final_guess, confidence_level = find_most_likely_classification(neural_network_guesses)


print("The most likely classification is: " + str(final_guess))
print("The confidence level is: " + str(confidence_level) + "%")