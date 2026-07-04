Here is the Python code for the problem you described:

import random

def pick_coins(n):
    coins = [random.uniform(0, 1) for _ in range(2 * n)]
    coins.sort(reverse=True)
    return coins[:n]

def simulate_tosses(coins):
    heads = 0
    for coin in coins:
        if random.random() < coin:
            heads += 1
    return heads

def main():
    n = int(input("Enter the value of n: "))
    selected_coins = pick_coins(n)
    print("Selected coins:", selected_coins)

    num_simulations = 100000
    heads_count = 0
    for _ in range(num_simulations):
        if simulate_tosses(selected_coins) == n:
            heads_count += 1
    probability = heads_count / num_simulations
    print("Probability of getting n heads:", probability)

if __name__ == "__main__":
    main()