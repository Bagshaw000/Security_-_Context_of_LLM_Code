import itertools

def soln(n):
    coins = [i/(2*n) for i in range(1, 2*n+1)]
    return max([(sum(p), p) for p in itertools.combinations(coins, n)], key=lambda x: x[0])[1]