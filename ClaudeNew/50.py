import csv
import os

print("Welcome to the Pattern Learning Program!")
print("This program learns to recognize patterns, like how you recognize themes in literature.")
print()

def create_sample_data():
    print("Step 1: Creating a simple list of examples to learn from")
    print("(This is like creating a list in Excel)")
    print()
    
    examples = [
        ["happy", "good"],
        ["sad", "bad"],
        ["joyful", "good"],
        ["miserable", "bad"],
        ["cheerful", "good"],
        ["gloomy", "bad"]
    ]
    
    return examples

def show_the_data(data):
    print("Step 2: Let's look at our examples:")
    print("(Just like viewing data in Excel)")
    print()
    
    for row in data:
        print(f"Word: '{row[0]}' -> Type: '{row[1]}'")
    print()

def count_patterns(data):
    print("Step 3: Finding patterns in the examples")
    print("(Like looking for common themes in stories)")
    print()
    
    good_words = []
    bad_words = []
    
    for example in data:
        word = example[0]
        word_type = example[1]
        
        if word_type == "good":
            good_words.append(word)
        elif word_type == "bad":
            bad_words.append(word)
    
    print("Words marked as 'good':", good_words)
    print("Words marked as 'bad':", bad_words)
    print()
    
    return good_words, bad_words

def predict_new_word(word, good_words, bad_words):
    print(f"Step 4: Trying to classify a new word: '{word}'")
    print("(Like predicting what theme a new passage belongs to)")
    print()
    
    word_lower = word.lower()
    
    if word_lower in good_words:
        prediction = "good"
        confidence = "very confident"
    elif word_lower in bad_words:
        prediction = "bad"
        confidence = "very confident"
    else:
        prediction = "unknown"
        confidence = "not confident (we haven't seen this word before)"
    
    print(f"Prediction: The word '{word}' seems to be '{prediction}'")
    print(f"Confidence: {confidence}")
    print()
    
    return prediction

def save_results(good_words, bad_words):
    print("Step 5: Saving what we learned to a file")
    print("(Like saving your work in Word)")
    print()
    
    filename = "learned_patterns.txt"
    
    file = open(filename, "w")
    
    file.write("Patterns Learned from Examples\n")
    file.write("=" * 40 + "\n\n")
    file.write("Good words we learned:\n")
    for word in good_words:
        file.write(f"  - {word}\n")
    
    file.write("\nBad words we learned:\n")
    for word in bad_words:
        file.write(f"  - {word}\n")
    
    file.close()
    
    print(f"Results saved to '{filename}'")
    print()

def run_program():
    print("=" * 50)
    print("SIMPLE PATTERN LEARNING PROGRAM")
    print("=" * 50)
    print()
    
    data = create_sample_data()
    
    show_the_data(data)
    
    good_words, bad_words = count_patterns(data)
    
    test_words = ["wonderful", "terrible", "excellent", "awful", "mysterious"]
    
    print("Testing our learning on new words:")
    print()
    for test_word in test_words:
        predict_new_word(test_word, good_words, bad_words)
    
    save_results(good_words, bad_words)
    
    print("=" * 50)
    print("Program complete!")
    print("=" * 50)

if __name__ == "__main__":
    run_program()