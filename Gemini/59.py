

guesses = ["Golden Retriever", "Golden Retriever", "Labrador", "Golden Retriever", "Cat"]



most_likely_answer = max(set(guesses), key=guesses.count)


count_for_winner = guesses.count(most_likely_answer)


total_guesses = len(guesses)



confidence_level = (count_for_winner / total_guesses) * 100


print("The most likely classification is: " + str(most_likely_answer))
print("Confidence Level: " + str(confidence_level) + "%")