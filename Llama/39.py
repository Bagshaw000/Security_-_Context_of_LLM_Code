import math
import random

def calculate_combinations(n, k):
    return math.comb(n, k)

combinations = calculate_combinations(6, 2)

def complexity_function(combination):
    count = 0
    for i in range(len(combination)):
        for j in range(i+1, len(combination)):
            if combination[i] == combination[j]:
                count += 1
    return count

class Combination:
    def __init__(self, combinations):
        self.combinations = combinations
        self.triviality_rating = None
        self.complexity_rating = None
        self.classify()

    def classify(self):
        if len(set(self.combinations)) == 2 and set(self.combinations).pop() == "":
            self.triviality_rating = "Trivial"
            self.complexity_rating = "Simple"
        else:
            complexity = self.complexity_function(self.combinations)
            if complexity > 5:
                self.triviality_rating = "Non-trivial"
                self.complexity_rating = str(complexity) + " complex"
            elif complexity == 0:
                self.triviality_rating = "Trivial"
                self.complexity_rating = "Simple"
            else:
                self.triviality_rating = "Non-trivial"
                self.complexity_rating = str(complexity) + " complex"

combinations_list = [str(i) for i in range(6)]
random.shuffle(combinations_list)
combination_list = [''.join(x) for x in combinations_list]

combinations_list = []

for combination in combination_list:
    new_combination = list(combination)
    while len(set(new_combination)) != 2:
        if new_combination[0] == new_combination[-1]:
            new_combination.pop(-1)
    new_combinations = calculate_combinations(6, len(new_combination))
    for i in range(new_combinations):
        combination_list.append(''.join(random.sample(list(new_combination), len(new_combination))))
        combinations_list.append Combination(combination_list[i])

for c in combinations_list:
    print(c.__dict__)