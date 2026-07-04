import pygame
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDE_MARGIN = 50
BOARD_GAP = 50


SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]


COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

class TetrisEngine:
    
    def __init__(self, x_offset):
        self.grid = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.x_offset = x_offset
        self.current_piece = Tetromino(random.choice(SHAPES))
        self.next_piece = Tetromino(random.choice(SHAPES))
        self.score = 0
        self.game_over = False

    def check_collision(self, piece, offset_x=0, offset_y=0, shape=None):
        shape = shape or piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x] != (0, 0, 0):
                        return True
        return False

    def rotate(self):
        
        new_shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        if not self.check_collision(self.current_piece, shape=new_shape):
            self.current_piece.shape = new_shape

    def move(self, dx, dy):
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        if dy > 0:
            self.lock_piece()
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    
                    if self.current_piece.y + y < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(random.choice(SHAPES))
        
        if self.check_collision(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        
        new_grid = [row for row in self.grid if any(cell == (0, 0, 0) for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [(0, 0, 0) for _ in range(GRID_WIDTH)])
        self.grid = new_grid
        self.score += lines_cleared * 100

    def draw(self, surface):
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = (self.x_offset + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, self.grid[y][x], rect)
                pygame.draw.rect(surface, (40, 40, 40), rect, 1)

        
        if not self.game_over:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        rect = (self.x_offset + (self.current_piece.x + x) * BLOCK_SIZE,
                                (self.current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(surface, self.current_piece.color, rect)

        
        font = pygame.font.SysFont('consolas', 18)
        score_label = font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_label, (self.x_offset, GRID_HEIGHT * BLOCK_SIZE + 10))
        if self.game_over:
            over_label = font.render("GAME OVER", True, (255, 50, 50))
            surface.blit(over_label, (self.x_offset, GRID_HEIGHT * BLOCK_SIZE + 35))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Triple Tetris - 3 Player Local")
    clock = pygame.time.Clock()

    
    players = [
        TetrisEngine(SIDE_MARGIN),
        TetrisEngine(SIDE_MARGIN + (GRID_WIDTH * BLOCK_SIZE) + BOARD_GAP),
        TetrisEngine(SIDE_MARGIN + 2 *