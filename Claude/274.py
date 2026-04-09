import random

def pick_coins(n):
    coins = [(random.random(), i) for i in range(2*n)]
    coins.sort(reverse=True)
    return [coin[1] for coin in coins[:n]]