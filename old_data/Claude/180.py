def blokus_duo_pieces():
    pieces = []
    
    
    pieces.append([(0,0)])
    
    
    pieces.append([(0,0), (1,0)])
    
    
    pieces.append([(0,0), (1,0), (2,0)])
    pieces.append([(0,0), (0,1), (0,2)])
    
    
    pieces.append([(0,0), (1,0), (2,0), (3,0)])
    pieces.append([(0,0), (0,1), (0,2), (0,3)])
    pieces.append([(0,0), (0,1), (1,0), (1,1)])
    pieces.append([(0,0), (0,1), (1,1), (1,2)])
    
    
    pieces.append([(0,0), (1,0), (2,0), (3,0), (4,0)])
    pieces.append([(0,0), (0,1), (0,2), (0,3), (0,4)])
    pieces.append([(0,0), (0,1), (1,0), (1,1), (2,0)])
    pieces.append([(0,0), (0,1), (0,2), (1,0), (1,1)])
    pieces.append([(0,0), (0,1), (1,0), (1,1), (1,2)])
    
    return pieces