def blokus_duo_pieces():
    pieces = []
    
    
    pieces.append((1,))
    
    
    pieces.append((1,1))
    
    
    pieces.append((1,1,1))
    pieces.append((1,1,0))
    
    
    pieces.append((1,1,1,1))
    pieces.append((1,1,1,0))
    pieces.append((1,1,0,0))
    pieces.append((1,0,1,0))
    
    
    pieces.append((1,1,1,1,1))
    pieces.append((1,1,1,1,0))
    pieces.append((1,1,1,0,0))
    pieces.append((1,1,0,0,0))
    pieces.append((1,0,1,0,0))
    pieces.append((1,0,0,1,0))
    
    return pieces

def blokus_duo_possibilities(pieces):
    possibilities = 0
    for piece in pieces:
        possibilities += 4 * len(set(piece))
    return possibilities

pieces = blokus_duo_pieces()
print(len(pieces))
print(blokus_duo_possibilities(pieces))