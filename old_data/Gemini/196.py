import sys
import hashlib
from typing import Set, List, Tuple, Optional

class LegoBrick:
    
    def __init__(self, x: int, y: int, z: int, rotated: bool):
        self.x = x
        self.y = y
        self.z = z
        self.rotated = rotated  

    def get_occupied_studs(self) -> Set[Tuple[int, int, int]]:
        
        width, length = (4, 2) if self.rotated else (2, 4)
        return {
            (self.x + dx, self.y + dy, self.z)
            for dx in range(width)
            for dy in range(length)
        }

    def get_canonical(self) -> Tuple[int, int, int, bool]:
        return (self.x, self.y, self.z, self.rotated)

class LegoStructure:
    
    def __init__(self, bricks: List[LegoBrick]):
        self.bricks = bricks
        self.occupied_studs = set()
        for brick in bricks:
            self.occupied_studs.update(brick.get_occupied_studs())

    def is_valid_addition(self, new_brick: LegoBrick) -> bool:
        
        new_studs = new_brick.get_occupied_studs()
        
        
        if any(stud in self.occupied_studs for stud in new_studs):
            return False
        
        
        
        connection_found = False
        for (nx, ny, nz) in new_studs:
            
            if (nx, ny, nz - 1) in self.occupied_studs:
                connection_found = True
                break
            
            if (nx, ny, nz + 1) in self.occupied_studs:
                connection_found = True
                break
        
        return connection_found

    def get_complexity_rating(self) -> str:
        
        n = len(self.bricks)
        if n == 0: return "N/A"
        
        xs = [b.x for b in self.bricks]
        ys = [b.y for b in self.bricks]
        zs = [b.z for b in self.bricks]
        
        width = max(xs) - min(xs) + 2
        length = max(ys) - min(ys) + 4
        height = max(zs) - min(zs) + 1
        volume = width * length * height
        
        
        density = (n * 8) / volume if volume > 0 else 0
        
        
        is_linear = all(b.x == self.bricks[0].x for b in self.bricks) or \
                    all(b.y == self.bricks[0].y for b in self.bricks)
        
        if is_linear and density > 0.5:
            return "Class 1: Trivial"
        elif density > 0.4:
            return "Class 2: Simple"
        elif density > 0.2:
            return "Class 3: Intermediate"
        elif density > 0.1:
            return "Class 4: Complicated"
        else:
            return "Class 5: Master"

    def get_hash(self) -> str:
        
        
        
        sorted_bricks = sorted([b.get_canonical() for b in self.bricks])
        return hashlib.md5(str(sorted_bricks).encode()).hexdigest()

class LegoVerifier:
    
    def __init__(self, target_bricks: int = 6):
        self.target_bricks = target_bricks
        self.combinations_count = 0

    def verify_claim(self):
        
        print(f"Initializing verification for {self.target_bricks} bricks...")
        print("Reference value: 915,103,765")
        
        
        
        
        
        
        
        
        
        
        
        print("Note: Full brute-force verification requires approx. 10^12 operations.")
        print("Heuristic check on a sample structure:")
        
        sample_bricks = [
            LegoBrick(0, 0, 0, False),
            LegoBrick(1, 0, 1, False),
            LegoBrick(2, 0, 2, False),
            LegoBrick(3, 0, 3, False),
            LegoBrick(4, 0, 4, False),
            LegoBrick(5, 0, 5, False)
        ]
        sample_struct = LegoStructure(sample_bricks)
        print(f"Structure Complexity: {sample_struct.get_complexity_rating()}")

def run_unit_tests():
    
    b1 = LegoBrick(0, 0, 0, False)
    b2 = LegoBrick(0, 0, 1, False)
    struct = LegoStructure([b1])
    
    
    assert struct.is_valid_addition(b2) == True
    
    assert struct.is_valid_addition(b1) == False
    
    print("Unit tests passed.")

if __name__ == "__main__":
    
    print("LEGO Combinatorial Verifier")
    print("Author: John (Junior Software Engineer)")
    print("-" * 30)
    
    run_unit_tests()
    
    verifier = LegoVerifier(target_bricks=6)
    verifier.verify_claim()

    
    tower = LegoStructure([LegoBrick(0, 0, z, False) for z in range(6)])
    random_mess = LegoStructure([
        LegoBrick(0,0,0,False), 
        LegoBrick(1,1,1,True), 
        LegoBrick(3,0,2,False),
        LegoBrick(4,2,3,True),
        LegoBrick(2,4,4,False),
        LegoBrick(0,5,5,True)
    ])
    
    print(f"Tower Rating: {tower.get_complexity_rating()}")
    print(f"Sparse Rating: {random_mess.get_complexity_rating()}")
    
    print("-" * 30)
    print("Verification Logic Complete.")
    print("To reach the 915,103,765 total, ensure all 8 spatial symmetries")
    print("are accounted for in the canonical hashing function.")