

guesses = ["Cat", "Cat", "Dog", "Cat", "Bird"]



most_likely_classification = max(set(guesses), key=guesses.count)



count_of_top_guess = guesses.count(most_likely_classification)
total_number_of_guesses = len(guesses)
confidence_percentage = (count_of_top_guess / total_number_of_guesses) * 100


print("Final Decision: " + str(most_likely_classification))
print("Confidence Level: " + str(confidence_percentage) + "%")