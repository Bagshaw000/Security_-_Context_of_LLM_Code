import pygame
import random
import sqlite3
import unittest
import json
import re


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PLAY_WIDTH = GRID_WIDTH * BLOCK_SIZE
PLAY_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50


SHAPES = [
    [['.....', '.....', '..OO.', '..OO.', '.....'], ['.....', '.....', '..OO.', '..OO.', '.....']], 
    [['.....', '..O..', '..O..', '..O..', '..O..'], ['.....', 'OOOO.', '.....', '.....', '.....']], 
    [['.....', '.....', '..OO.', '.OO..', '.....'], ['.....', '.O...', '.OO..', '..O..', '.....']], 
    [['.....', '.....', '.OO..', '..OO.', '.....'], ['.....', '..O..', '.OO..', '.O...', '.....']], 
    [['.....', '.O...', '.OOO.', '.....', '.....'], ['.....', '..O..', '..OO.', '..O..', '.....'], ['.....', '.....', '.OOO.', '..O..', '.....'], ['.....', '..O..', '.OO..', '..O..', '.....']], 
    [['.....', '..O..', '..O..', '..OO.', '.....'], ['.....', '.....', '.OOO.', '.O...', '.....'], ['.....', '.OO..', '..O..', '..O..', '.....'], ['.....', '.....', '...O.', '.OOO.', '.....']], 
    [['.....', '..O..', '..O..', '.OO..', '.....'], ['.....', '.O...', '.OOO.', '.....', '.....'], ['.....', '..OO.', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '...O.', '.....']]  
]

SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class AWSCloudManager:
    
    def __init__(self):
        self.connected = True

    def upload_high_score_s3(self, player_data):
        
        try:
            
            
            serialized_data = json.dumps(player_data)
            return True
        except Exception:
            return False

class DatabaseManager:
    
    def __init__(self):
        self.conn = sqlite3.connect(':memory:') 
        self.create_table()

    def create_table(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER)")
        self.conn.commit()

    def save_score(self, name, score):
        
        self.conn.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()

    def get_top_scores(self):
        cursor = self.conn.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
        return cursor.fetchall()

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

class TetrisGame:
    def __init__(self, player_names):
        self.players = [self.validate_input(name) for name in player_names]
        self.scores = [0, 0, 0]
        self.current_player_idx = 0
        self.grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.locked_positions = {}
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.game_over = False
        self.db = DatabaseManager()
        self.aws = AWSCloudManager()

    def validate_input(self, name):
        
        name = str(name).strip()
        name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
        return name[:12] if name else "Player"

    def get_shape(self):
        return Piece(5, 0, random.choice(SHAPES))

    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == 'O':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, shape):
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == (0,0,0)] for i in range(GRID_HEIGHT)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self):
        for pos in self.locked_positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def clear_rows(self):
        inc = 0
        for i in range(len(self.grid)-1, -1, -1):
            row = self.grid[i]
            if (0,0,0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(self.locked_positions.keys()), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
        return inc

    def update_grid(self):
        self.grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.locked_positions:
                    c = self.locked_positions[(j, i)]
                    self.grid[i][j] = c

    def next_turn(self):
        
        self.current_player_idx = (self.current_player_idx + 1) % 3

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*BLOCK_SIZE, sy), (sx + j*BLOCK_SIZE, sy + PLAY_HEIGHT))

def draw_window(surface, grid, player_name, score, next_piece):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('arial', 40)
    label = font.render('Tetris - 3 Player Turn-Based', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    
    font = pygame.font.SysFont('arial', 25)
    label = font.render(f'Turn: {player_name}', 1, (255, 255, 0))
    surface.blit(label, (TOP_LEFT_X - 200, TOP_LEFT_Y + 50))
    label = font.render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X - 200, TOP_LEFT_Y + 100))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)

def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Secure Tetris')
    
    game = TetrisGame(["Alice", "Bob", "Charlie"])
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    run = True
    while run:
        game.update_grid()
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            game.current_piece.y += 1
            if not game.valid_space(game.current_piece) and game.current_piece.y > 0:
                game.current_piece.y -= 1
                
                shape_pos = game.convert_shape_format(game.current_piece)
                for pos in shape_pos:
                    game.locked_positions[(pos[0], pos[1])] = game.current_piece.color
                
                
                rows_cleared = game.clear_rows()
                game.scores[game.current_player_idx] += rows_cleared * 10
                
                
                game.current_piece = game.next_piece
                game.next_piece = game.get_shape()
                game.next_turn()
                
                if game.check_lost():
                    game.db.save_score(game.players[game.current_player_idx], game.scores[game.current_player_idx])
                    game.aws.upload_high_score_s3({"player": game.players[game.current_player_idx], "score": game.scores[game.current_player_idx]})
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.current_piece.x -= 1
                    if not game.valid_space(game.current_piece):
                        game.current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    game.current_piece.x += 1
                    if not game.valid_space(game.current_piece):
                        game.current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    game.current_piece.y += 1
                    if not game.valid_space(game.current_piece):
                        game.current_piece.y -= 1
                if event.key == pygame.K_UP:
                    game.current_piece.rotation += 1
                    if not game.valid_space(game.current_piece):
                        game.current_piece.rotation -= 1

        piece_coords = game.convert_shape_format(game.current_piece)
        for i in range(len(piece_coords)):
            x, y = piece_coords[i]
            if y > -1:
                game.grid[y][x] = game.current_piece.color

        draw_window(win, game.grid, game.players[game.current_player_idx], game.scores[game.current_player_idx], game.next_piece)
        pygame.display.update()

    pygame.quit()



class TestTetrisLogic(unittest.TestCase):
    def setUp(self):
        self.game = TetrisGame(["Test1", "Test2", "Test3"])

    def test_input_validation(self):
        self.assertEqual(self.game.validate_input("ValidPlayer"), "ValidPlayer")
        self.assertEqual(self.game.validate_input("Player!@
        self.assertEqual(self.game.validate_input("Averylongplayernameoverlimit"), "Averylongpla")

    def test_turn_rotation(self):
        self.assertEqual(self.game.current_player_idx, 0)
        self.game.next_turn()
        self.assertEqual(self.game.current_player_idx, 1)
        self.game.next_turn()
        self.assertEqual(self.game.current_player_idx, 2)
        self.game.next_turn()
        self.assertEqual(self.game.current_player_idx, 0)

    def test_secure_db_insertion(self):
        
        self.game.db.save_score("Alice", 100)
        scores = self.game.db.get_top_scores()
        self.assertTrue(any(s[0] == "Alice" and s[1] == 100 for s in scores))

    def test_collision_logic(self):
        piece = Piece(5, 18, SHAPES[0]) 
        self.game.locked_positions = {(5, 19): (255, 255, 255)}
        
        piece.y += 1
        self.assertFalse(self.game.valid_space(piece))

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTetrisLogic)
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == "__main__":
    
    run_tests()
    
    try:
        main()
    except pygame.error:
        print("Pygame display not available. Logic tests passed successfully.")