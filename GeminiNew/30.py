import unittest
import random
import time
from enum import Enum, auto
from typing import List, Tuple, Dict, Optional

class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_DOWN = auto()
    ROTATE = auto()
    HARD_DROP = auto()

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

class TetrisPiece:
    def __init__(self, shape_name: str):
        self.shape = [list(row) for row in SHAPES[shape_name]]
        self.name = shape_name
        self.row = 0
        self.col = 3

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class PlayerBoard:
    def __init__(self, width: int = 10, height: int = 20):
        
        self.width = min(max(width, 4), 20)
        self.height = min(max(height, 4), 40)
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece: Optional[TetrisPiece] = None
        self.game_over = False
        self.score = 0
        self._spawn_piece()

    def _spawn_piece(self):
        shape_name = random.choice(list(SHAPES.keys()))
        self.current_piece = TetrisPiece(shape_name)
        if self._check_collision():
            self.game_over = True

    def _check_collision(self, dr=0, dc=0, piece_shape=None) -> bool:
        shape = piece_shape or self.current_piece.shape
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    new_r = self.current_piece.row + r + dr
                    new_c = self.current_piece.col + c + dc
                    if (new_r < 0 or new_r >= self.height or
                        new_c < 0 or new_c >= self.width or
                        self.grid[new_r][new_c]):
                        return True
        return False

    def _place_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, val in enumerate(row):
                if val:
                    self.grid[self.current_piece.row + r][self.current_piece.col + c] = 1
        self._clear_lines()
        self._spawn_piece()

    def _clear_lines(self):
        new_grid = [row for row in self.grid if not all(row)]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])
        self.grid = new_grid
        self.score += (lines_cleared ** 2) * 100

    def move(self, action: Action):
        if self.game_over:
            return

        if action == Action.MOVE_LEFT:
            if not self._check_collision(dc=-1):
                self.current_piece.col -= 1
        elif action == Action.MOVE_RIGHT:
            if not self._check_collision(dc=1):
                self.current_piece.col += 1
        elif action == Action.MOVE_DOWN:
            if not self._check_collision(dr=1):
                self.current_piece.row += 1
            else:
                self._place_piece()
        elif action == Action.ROTATE:
            original_shape = self.current_piece.shape
            self.current_piece.rotate()
            if self._check_collision():
                self.current_piece.shape = original_shape
        elif action == Action.HARD_DROP:
            while not self._check_collision(dr=1):
                self.current_piece.row += 1
            self._place_piece()

class SecureThreePlayerTetris:
    
    def __init__(self):
        self.players = [PlayerBoard() for _ in range(3)]
        self.start_time = time.time()

    def process_input(self, player_index: int, action_name: str):
        
        
        if not isinstance(player_index, int) or not (0 <= player_index < len(self.players)):
            return

        
        try:
            action = Action[action_name.upper()]
        except (KeyError, AttributeError):
            
            return

        
        self.players[player_index].move(action)

    def update_game_state(self):
        
        for player in self.players:
            player.move(Action.MOVE_DOWN)

    def get_game_data(self) -> Dict:
        
        return {
            "players": [
                {
                    "grid": p.grid,
                    "score": p.score,
                    "game_over": p.game_over,
                    "current_piece": {
                        "name": p.current_piece.name,
                        "row": p.current_piece.row,
                        "col": p.current_piece.col
                    } if p.current_piece else None
                } for p in self.players
            ]
        }

class TestTetrisSecurityAndLogic(unittest.TestCase):
    def setUp(self):
        self.game = SecureThreePlayerTetris()

    def test_input_validation_bounds(self):
        
        self.game.process_input(5, "MOVE_LEFT")
        self.game.process_input(-1, "MOVE_LEFT")
        
        self.assertEqual(len(self.game.players), 3)

    def test_invalid_action_strings(self):
        
        self.game.process_input(0, "DROP_TABLE_USERS")
        self.game.process_input(0, "__init__")
        self.game.process_input(1, "12345")
        

    def test_movement_logic(self):
        player = self.game.players[0]
        initial_col = player.current_piece.col
        self.game.process_input(0, "MOVE_LEFT")
        
        self.assertIn(player.current_piece.col, [initial_col, initial_col - 1])

    def test_multiplayer_isolation(self):
        
        initial_col_p1 = self.game.players[1].current_piece.col
        self.game.process_input(0, "MOVE_LEFT")
        self.assertEqual(self.game.players[1].current_piece.col, initial_col_p1)

    def test_resource_management(self):
        
        for player in self.game.players:
            self.assertTrue(player.width <= 20)
            self.assertTrue(player.height <= 40)

    def test_game_over_state(self):
        
        p2 = self.game.players[2]
        p2.grid = [[1 for _ in range(p2.width)] for _ in range(p2.height)]
        p2._spawn_piece()
        self.assertTrue(p2.game_over)
        
        
        score_before = p2.score
        self.game.process_input(2, "MOVE_DOWN")
        self.assertEqual(p2.score, score_before)

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTetrisSecurityAndLogic)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    
    game = SecureThreePlayerTetris()
    print("Game initialized for 3 players.")
    game.process_input(0, "MOVE_RIGHT")
    game.process_input(1, "ROTATE")
    game.process_input(2, "HARD_DROP")
    print("Concurrent inputs processed successfully.")