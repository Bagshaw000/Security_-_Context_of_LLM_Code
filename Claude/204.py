import itertools

def generate_combinations(num_bricks):
    bricks = ['0', '1']
    return len(list(itertools.product(bricks, repeat=num_bricks)))

def verify_lego_claim():
    num_bricks = 6
    total_combinations = 915103765
    calculated_combinations = generate_combinations(num_bricks)
    if calculated_combinations == total_combinations:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")

def classify_combinations(num_bricks):
    total_combinations = generate_combinations(num_bricks)
    trivial_threshold = total_combinations // 10
    complicated_threshold = total_combinations - trivial_threshold
    
    if total_combinations <= trivial_threshold:
        return "Trivial"
    elif total_combinations <= complicated_threshold:
        return "Moderate"
    else:
        return "Complicated"

verify_lego_claim()
print(classify_combinations(6))