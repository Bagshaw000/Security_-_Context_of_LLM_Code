import itertools
import math

def count_squares(n):
    total = 0
    for r in range(1, n+1):
        size = math.comb(r+1, 2)
        if r % 4 == 0 or r % 4 == 3:
            corners = math.comb(math.ceil(r/2)+1, 2)
            sides = size - corners
            total += (sides * sides) + (corners * corners)

    return total

def calculate_block_pieces(n):
    block_pieces = set()
    for r in range(1, n+1):
        size = math.comb(r+1, 2)
        if r % 4 == 0 or r % 4 == 3:
            corners = math.comb(math.ceil(r/2)+1, 2)
            sides = size - corners
            block_pieces.add(sides * sides + corners * corners)

    return len(block_pieces)

def calculate_total_pieces(n):
    total_pieces = count_squares(n) + n
    for r in range(1, n+1):
        size = math.comb(r+1, 2)
        if r % 4 == 0 or r % 4 == 3:
            corners = math.comb(math.ceil(r/2)+1, 2)
            sides = size - corners
            total_pieces += (sides * sides + corners * corners)

    return total_pieces

def calculate_total_possibilities(n):
    total_possibilities = pow(2, n) - 3*n
    for r in range(1, n+1):
        size = math.comb(r+1, 2)
        if r % 4 == 0 or r % 4 == 3:
            corners = math.comb(math.ceil(r/2)+1, 2)
            sides = size - corners
            total_possibilities -= (sides * sides + corners * corners)

    return total_possibilities

n = 5
total_pieces = calculate_total_pieces(n)
total_possibilities = calculate_total_possibilities(n)

print(f"Total pieces: {calculate_block_pieces(n)}")
print(f"Total possible combinations without cancelling out symmetries: {total_pieces}")
print(f"Total possible placements for any two pieces: {total_possibilities}")