import itertools
import random

class Brick:
    def __init__(self):
        pass

    def is_trivial(self, combination):
        return combination == tuple(sorted([1, 2, 3, 4, 5, 6])) or combination == tuple(sorted([2, 2, 2, 2, 2, 2]))

class Combination:
    def __init__(self, bricks):
        self.bricks = bricks

    def is_trivial(self):
        return Brick().is_trivial(self.bricks)

def calculate_combinations():
    brick_types = [i for i in range(1, 7)]
    combinations = list(itertools.permutations(brick_types))
    return len(combinations)

def classify_combination(combination):
    if combination.is_trivial():
        return 'trivial', '1'
    elif any(len(set(combination)) == 1 or len(set(combination)) <= 2 for combination in itertools.combinations(combination, 3)):
        return 'complicated', '5'
    else:
        return 'complicated', '4'

def main():
    total_combinations = calculate_combinations()
    print(f'Total combinations: {total_combinations}')
    valid_combinations = [Combination(random.sample(range(1, 7), random.randint(3, 6))) for _ in range(total_combinations)]
    result = {'trivial': 0, 'complicated': 0}
    for i, combination in enumerate(valid_combinations):
        result[classify_combination(combination)[1]] += 1
    print(f'Trivial combinations: {result["trivial"]}')
    print(f'Complicated combinations: {result["complicated"]}')

if __name__ == "__main__":
    main()