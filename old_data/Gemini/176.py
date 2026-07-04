







board_layout = [
    "r", "n", "b", "q", "k", "b", "n", "r",
    "p", "p", "p", "p", ".", "p", "p", "p",
    ".", ".", ".", ".", ".", ".", ".", ".",
    ".", ".", ".", ".", "p", ".", ".", ".",
    ".", ".", ".", ".", "P", ".", ".", ".",
    ".", ".", ".", ".", ".", ".", ".", ".",
    "P", "P", "P", "P", ".", "P", "P", "P",
    "R", "N", "B", "Q", "K", "B", "N", "R"
]





piece_values = {
    "P": 1,   "N": 3,   "B": 3,   "R": 5,   "Q": 9,   "K": 0,
    "p": -1,  "n": -3,  "b": -3,  "r": -5,  "q": -9,  "k": 0,
    ".": 0
}


evaluation_score = 0




for square in board_layout:
    piece_value = piece_values[square]
    evaluation_score = evaluation_score + piece_value






print("--- Chess Position Evaluation ---")
print("Total Material Score:", evaluation_score)

if evaluation_score > 0:
    print("Result: White has the material advantage.")
elif evaluation_score < 0:
    print("Result: Black has the material advantage.")
else:
    print("Result: The position is equal in material.")