import itertools
import math

class Combination:
    def __init__(self, sides):
        self.sides = sides
        self.rating = 0

def calculate_combinations(num_bricks):
    return math.comb(6 * num_bricks, 2 * num_bricks)

combinations = [calculate_combinations(i) for i in range(1, 7)]

for comb in combinations:
    if comb == 1:
        rating = 3
    elif comb == 2 or comb == 6:
        rating = 5
    elif comb > 2 and comb <= 4:
        rating = 8
    else:
        rating = 9

for i, comb in enumerate(combinations):
    combination = Combination(i+1)
    combination.sides = comb
    print(f"Combination {combination.sides} has a rating of {combination.rating}")