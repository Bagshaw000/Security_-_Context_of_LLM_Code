import sys
import logging
import unittest
from typing import Set, Tuple, List, FrozenSet
from dataclasses import dataclass
from collections import deque


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Brick:
    
    x: int
    y: int
    z: int
    orientation: int  

    def get_occupied_studs(self) -> Set[Tuple[int, int, int]]:
        
        studs = set()
        dx, dy = (2, 4) if self.orientation == 0 else (4, 2)
        for i in range(dx):
            for j in range(dy):
                studs.add((self.x + i, self.y + j, self.z))
        return studs

class Assembly:
    
    def __init__(self, bricks: FrozenSet[Brick]):
        self.bricks = bricks
        self._canonical_form = self._compute_canonical_form()

    def _compute_canonical_form(self) -> FrozenSet[Brick]:
        
        if not self.bricks:
            return frozenset()
        min_x = min(b.x for b in self.bricks)
        min_y = min(b.y for b in self.bricks)
        min_z = min(b.z for b in self.bricks)
        return frozenset(
            Brick(b.x - min_x, b.y - min_y, b.z - min_z, b.orientation)
            for b in self.bricks
        )

    def __hash__(self):
        return hash(self._canonical_form)

    def __eq__(self, other):
        if not isinstance(other, Assembly):
            return False
        return self._canonical_form == other._canonical_form

class ComplexityHeuristic:
    
    @staticmethod
    def classify(assembly: Assembly) -> str:
        
        if len(assembly.bricks) <= 1:
            return "Trivial"
        
        all_studs = []
        for brick in assembly.bricks:
            all_studs.extend(brick.get_occupied_studs())
        
        unique_studs = len(set(all_studs))
        total_potential_studs = len(assembly.bricks) * 8
        
        
        overlap_factor = (total_potential_studs - unique_studs) / len(assembly.bricks)
        
        return "Complicated" if overlap_factor > 1.5 else "Trivial"

class LegoCombinator:
    
    def __init__(self, max_bricks: int = 6):
        if not isinstance(max_bricks, int) or max_bricks < 1:
            raise ValueError("max_bricks must be a positive integer.")
        self.max_bricks = max_bricks

    def get_valid_placements(self, existing_bricks: FrozenSet[Brick]) -> List[Brick]:
        
        occupied_studs = set()
        for b in existing_bricks:
            occupied_studs.update(b.get_occupied_studs())

        possible_next_bricks = []
        
        
        
        min_x = min(b.x for b in existing_bricks) - 4
        max_x = max(b.x for b in existing_bricks) + 4
        min_y = min(b.y for b in existing_bricks) - 4
        max_y = max(b.y for b in existing_bricks) + 4
        min_z = min(b.z for b in existing_bricks) - 1
        max_z = max(b.z for b in existing_bricks) + 1

        for z in range(min_z, max_z + 1):
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    for orientation in [0, 1]:
                        new_brick = Brick(x, y, z, orientation)
                        new_studs = new_brick.get_occupied_studs()
                        
                        
                        if any((s[0], s[1], s[2]) in occupied_studs for s in new_studs):
                            continue
                        
                        
                        
                        connected = False
                        for (sx, sy, sz) in new_studs:
                            if (sx, sy, sz - 1) in occupied_studs or (sx, sy, sz + 1) in occupied_studs:
                                connected = True
                                break
                        
                        if connected:
                            possible_next_bricks.append(new_brick)
                            
        return possible_next_bricks

    def count_combinations(self) -> int:
        
        initial_brick = Brick(0, 0, 0, 0)
        initial_assembly = Assembly(frozenset([initial_brick]))
        
        
        seen_assemblies = {initial_assembly}
        current_layer = {initial_assembly}

        logger.info(f"Starting verification for {self.max_bricks} bricks...")

        for n in range(2, self.max_bricks + 1):
            next_layer = set()
            for assembly in current_layer:
                placements = self.get_valid_placements(assembly.bricks)
                for p in placements:
                    new_set = set(assembly.bricks)
                    new_set.add(p)
                    new_assembly = Assembly(frozenset(new_set))
                    next_layer.add(new_assembly)
            
            current_layer = next_layer
            logger.info(f"Layer {n}: Found {len(current_layer)} unique combinations.")
            
        return len(current_layer)

class TestLegoVerification(unittest.TestCase):
    
    
    def test_brick_studs(self):
        brick = Brick(0, 0, 0, 0)
        studs = brick.get_occupied_studs()
        self.assertEqual(len(studs), 8)
        self.assertIn((0, 0, 0), studs)
        self.assertIn((1, 3, 0), studs)

    def test_assembly_canonical_form(self):
        b1 = Brick(10, 10, 10, 0)
        b2 = Brick(0, 0, 0, 0)
        a1 = Assembly(frozenset([b1]))
        a2 = Assembly(frozenset([b2]))
        self.assertEqual(a1, a2)

    def test_heuristic_classification(self):
        
        b1 = Brick(0, 0, 0, 0)
        b2 = Brick(0, 0, 1, 0)
        stack = Assembly(frozenset([b1, b2]))
        rating = ComplexityHeuristic.classify(stack)
        self.assertIsInstance(rating, str)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            LegoCombinator(max_bricks=-1)



def run_production_verification():
    
    try:
        
        
        combinator = LegoCombinator(max_bricks=2)
        total = combinator.count_combinations()
        
        
        
        print(f"Verification complete. Total combinations for 2 bricks: {total}")
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLegoVerification)
    test_result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    if test_result.wasSuccessful():
        run_production_verification()
    else:
        sys.exit(1)