import collections
import itertools
import hashlib
from typing import Set, List, Tuple, FrozenSet

class Brick2x4:
    
    def __init__(self, x: int, y: int, z: int, orientation: int):
        self.x = x
        self.y = y
        self.z = z
        self.orientation = orientation  

    def get_occupied_studs(self) -> Set[Tuple[int, int, int]]:
        
        studs = set()
        dx, dy = (4, 2) if self.orientation == 0 else (2, 4)
        for i in range(dx):
            for j in range(dy):
                studs.add((self.x + i, self.y + j, self.z))
        return studs

    def __repr__(self):
        return f"Brick(x={self.x}, y={self.y}, z={self.z}, rot={self.orientation})"

class Configuration:
    
    def __init__(self, bricks: List[Brick2x4]):
        self.bricks = bricks
        self.stud_map = self._build_stud_map()

    def _build_stud_map(self) -> Set[Tuple[int, int, int]]:
        all_studs = set()
        for brick in self.bricks:
            all_studs.update(brick.get_occupied_studs())
        return all_studs

    def is_valid_connection(self, new_brick: Brick2x4) -> bool:
        
        new_studs = new_brick.get_occupied_studs()
        
        
        if any(stud in self.stud_map for stud in new_studs):
            return False
            
        
        connected = False
        for (x, y, z) in new_studs:
            if (x, y, z - 1) in self.stud_map or (x, y, z + 1) in self.stud_map:
                connected = True
                break
        return connected

    def get_canonical_id(self) -> str:
        
        variants = []
        
        
        for rot in range(4):
            variants.append(self._normalize([self._rotate_brick(b, rot) for b in self.bricks]))
        
        variants.sort()
        return hashlib.md5(str(variants[0]).encode()).hexdigest()

    def _rotate_brick(self, b: Brick2x4, turns: int) -> Tuple[int, int, int, int]:
        
        if turns == 0: return (b.x, b.y, b.z, b.orientation)
        if turns == 1: return (-b.y, b.x, b.z, 1 - b.orientation)
        if turns == 2: return (-b.x, -b.y, b.z, b.orientation)
        if turns == 3: return (b.y, -b.x, b.z, 1 - b.orientation)
        return (b.x, b.y, b.z, b.orientation)

    def _normalize(self, brick_tuples: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
        min_x = min(b[0] for b in brick_tuples)
        min_y = min(b[1] for b in brick_tuples)
        min_z = min(b[2] for b in brick_tuples)
        normalized = sorted([(b[0]-min_x, b[1]-min_y, b[2]-min_z, b[3]) for b in brick_tuples])
        return normalized

class ComplexityHeuristic:
    
    @staticmethod
    def rate(config: Configuration) -> Tuple[int, str]:
        bricks = config.bricks
        n = len(bricks)
        if n == 0: return (0, "Empty")

        
        height = max(b.z for b in bricks) - min(b.z for b in bricks) + 1
        footprint_x = max(b.x for b in bricks) - min(b.x for b in bricks)
        footprint_y = max(b.y for b in bricks) - min(b.y for b in bricks)
        spread = footprint_x * footprint_y
        
        
        cid_full = config.get_canonical_id()
        
        
        
        if height == n and spread <= 8:
            return (1, "Trivial: Simple Vertical Stack")
        
        if height == 1:
            return (2, "Simple: Single Layer Flat")
            
        if spread > n * 12:
            return (5, "Complicated: High Dispersion/Sparse Interlock")
            
        if height > 2 and spread > 16:
            return (4, "Advanced: Multi-level Branching")
            
        return (3, "Standard: Common Interlocking")

class LegoVerificationEngine:
    
    def __init__(self, target_n: int = 6):
        self.target_n = target_n
        self.memo = {}

    def verify_claim(self):
        
        print(f"Initializing verification for N={self.target_n} bricks...")
        
        
        initial_brick = Brick2x4(0, 0, 0, 0)
        current_configs = {Configuration([initial_brick]).get_canonical_id(): Configuration([initial_brick])}
        
        
        
        
        
        for i in range(2, self.target_n + 1):
            next_level_configs = {}
            for config_hash, config in current_configs.items():
                
                possible_moves = self._generate_possible_moves(config)
                for move in possible_moves:
                    new_bricks = config.bricks + [move]
                    new_config = Configuration(new_bricks)
                    new_hash = new_config.get_canonical_id()
                    if new_hash not in next_level_configs:
                        next_level_configs[new_hash] = new_config
            
            current_configs = next_level_configs
            print(f"Level {i}: Found {len(current_configs)} unique combinations.")
            
        return len(current_configs)

    def _generate_possible_moves(self, config: Configuration) -> List[Brick2x4]:
        moves = []
        
        min_x = min(b.x for b in config.bricks) - 4
        max_x = max(b.x for b in config.bricks) + 4
        min_y = min(b.y for b in config.bricks) - 4
        max_y = max(b.y for b in config.bricks) + 4
        min_z = min(b.z for b in config.bricks) - 1
        max_z = max(b.z for b in config.bricks) + 1

        for z in range(min_z, max_z + 1):
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    for rot in [0, 1]:
                        candidate = Brick2x4(x, y, z, rot)
                        if config.is_valid_connection(candidate):
                            moves.append(candidate)
        return moves

def run_demonstration():
    
    engine = LegoVerificationEngine(target_n=2)
    
    count = engine.verify_claim()
    
    
    
    b1 = Brick2x4(0, 0, 0, 0)
    b2 = Brick2x4(1, 1, 1, 1)
    b3 = Brick2x4(2, 0, 2, 0)
    complex_config = Configuration([b1, b2, b3])
    
    rating, description = ComplexityHeuristic.rate(complex_config)
    
    print("-" * 30)
    print(f"Verification Results (Small Scale N=2): {count} (Expected: 24)")
    print(f"Claim for N=6: 915,103,765")
    print("-" * 30)
    print(f"Heuristic Analysis Example:")
    print(f"Configuration: {complex_config.bricks}")
    print(f"Class Rating: {rating}")
    print(f"Complexity Label: {description}")

if __name__ == "__main__":
    
    
    run_demonstration()