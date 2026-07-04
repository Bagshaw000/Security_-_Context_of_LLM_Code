




guesses_from_programs = ["Cat", "Dog", "Cat", "", "!!!", "A_Very_Long_Nonsense_Word_That_Is_Invalid", "Cat", "Dog"]


valid_guesses = []

for item in guesses_from_programs:
    
    text = str(item).strip()
    
    
    if not text:
        continue
        
    
    if len(text) > 20:
        continue
        
    
    if not text.isalnum():
        continue
        
    
    
    valid_guesses.append(text.lower())


if not valid_guesses:
    print("Result: No valid guesses were provided to analyze.")
else:
    
    tally = {}
    for word in valid_guesses:
        if word in tally:
            tally[word] += 1
        else:
            tally[word] = 1

    
    winner = max(tally, key=tally.get)
    votes_for_winner = tally[winner]
    total_valid_votes = len(valid_guesses)

    
    
    certainty_percentage = (votes_for_winner / total_valid_votes) * 100

    
    print("Final Determination: " + winner.capitalize())
    print("Level of Agreement: " + str(round(certainty_percentage, 1)) + "%")