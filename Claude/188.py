n = 5
pieces = []
for i in range(1, n+1):
    if i == 1:
        pieces.append(1)
    elif i == 2:
        pieces.append(1)
    else:
        total = 0
        for j in range(1, i//2 + 1):
            total += 1
        pieces.append(total)
print(sum(pieces))