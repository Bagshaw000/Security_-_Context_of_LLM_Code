class LegoBrickCombinations:
    def __init__(self, num_bricks):
        self.num_bricks = num_bricks
        self.combinations = 0

    def calculate_combinations(self):
        
        self.combinations = 0
        for orientation in range(2):  
            self.combinations += self._count_combinations(orientation, self.num_bricks)
        return self.combinations

    def _count_combinations(self, orientation, remaining_bricks):
        if remaining_bricks == 0:
            return 1
        total = 0
        for i in range(1, remaining_bricks + 1):
            total += self._count_combinations(orientation, remaining_bricks - i)
        return total

    def classify_combination(self, combination):
        if combination < 100:
            return "Trivial"
        elif combination < 10000:
            return "Moderate"
        else:
            return "Complicated"


lego = LegoBrickCombinations(6)
calculated_combinations = lego.calculate_combinations()
print(f"Calculated combinations: {calculated_combinations}")
print(f"LEGO's claim verified: {calculated_combinations == 915103765}")


combination_example = 15000
classification = lego.classify_combination(combination_example)
print(f"Combination {combination_example} is classified as: {classification}")