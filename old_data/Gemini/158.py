import pygame
import random
from typing import List, Tuple, Optional


BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PADDING = 50
FPS = 60


BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  
    (255, 255, 0),  
    (128, 0, 128),  
    (0, 255, 0),    
    (255, 0, 0),    
    (0, 0, 255),    
    (255, 165, 0)   
]


SHAPES = [
    [[1, 1, 1, 1]],                                 
    [[1, 1], [1, 1]],                               
    [[0, 1, 0], [1, 1, 1]],                         
    [[0, 1, 1], [1, 1, 0]],                         
    [[1, 1, 0], [0, 1, 1]],                         
    [[1, 0, 0], [1, 1, 1]],                         
    [[0, 0, 1], [1, 1, 1]]                          
]

class Tetromino:
    def __init__(self, x: int, y: int, shape: List[List[int]]):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)

    def rotate(self):
        
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class PlayerBoard:
    def __init__(self, offset_x: int, player_name: str, controls: dict):
        self.offset_x = offset_x
        self.player_name = player_name
        self.controls = controls
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self._new_piece()
        self.score = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500  

    def _new_piece(self) -> Tetromino:
        shape = random.choice(SHAPES)
        return Tetromino(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape)

    def _check_collision(self, piece: Tetromino, dx=0, dy=0, shape=None) -> bool:
        shape = shape or piece.shape
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = piece.x + col_idx + dx
                    new_y = piece.y + row_idx + dy
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def _lock_piece(self):
        for row_idx, row in enumerate(self.current_piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    y = self.current_piece.y + row_idx
                    x = self.current_piece.x + col_idx
                    if y < 0:
                        self.game_over = True
                        return
                    self.grid[y][x] = self.current_piece.color
        
        self._clear_lines()
        self.current_piece = self._new_piece()
        if self._check_collision(self.current_piece):
            self.game_over = True

    def _clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(GRID_WIDTH)])
        self.grid = new_grid
        self.score += (lines_cleared ** 2) * 100

    def move(self, dx: int, dy: int):
        if self.game_over: return
        if not self._check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
        elif dy > 0:
            self._lock_piece()

    def rotate(self):
        if self.game_over: return
        rotated = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        if not self._check_collision(self.current_piece, shape=rotated):
            self.current_piece.shape = rotated

    def update(self, dt_ms: int):
        if self.game_over: return
        self.fall_time += dt_ms
        if self.fall_time >= self.fall_speed:
            self.move(0, 1)
            self.fall_time = 0

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        
        rect = pygame.Rect(self.offset_x, PADDING, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(surface, GRAY, rect, 1)

        
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(surface, color, 
                        (self.offset_x + x * BLOCK_SIZE, PADDING + y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        
        if not self.game_over:
            for row_idx, row in enumerate(self.current_piece.shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(surface, self.current_piece.color,
                            (self.offset_x + (self.current_piece.x + col_idx) * BLOCK_SIZE,
                             PADDING + (self.current_piece.y + row_idx) * BLOCK_SIZE,
                             BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        
        name_surf = font.render(self.player_name, True, WHITE)
        score_surf = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(name_surf, (self.offset_x, 10))
        surface.blit(score_surf, (self.offset_x, PADDING + GRID_HEIGHT * BLOCK_SIZE + 10))
        
        if self.game_over:
            over_surf = font.render("GAME OVER", True, (255, 0, 0))
            surface.blit(over_surf, (self.offset_x + 20, PADDING + (GRID_HEIGHT * BLOCK_SIZE) // 2))

def main():
    pygame.init()
    
    window_width = (GRID_WIDTH * BLOCK_SIZE * 3) + (PADDING * 4)
    window_height = (GRID_HEIGHT * BLOCK_SIZE) + (PADDING * 2) + 50
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Three-Player Tetris - Amazon Device Systems Engineering")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 18, bold=True)

    
    
    
    
    players = [
        PlayerBoard(PADDING, "Player 1 (Arrows)", {
            pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_DOWN: (0, 1), pygame.K_UP: "rotate"
        }),
        PlayerBoard(PADDING * 2 + GRID_WIDTH * BLOCK_SIZE, "Player 2 (WASD)", {
            pygame.K_a: (-1, 0), pygame.K_d: (1, 0), pygame.K_s: (0, 1), pygame.K_w: "rotate"
        }),
        PlayerBoard(PADDING * 3 + GRID_WIDTH * BLOCK_SIZE * 2, "Player 3 (IJKL)", {
            pygame.K_j: (-1, 0), pygame.K_l: (1, 0), pygame.K_k: (0, 1), pygame.K_i: "rotate"
        })
    ]

    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                for p in players:
                    if event.key in p.controls:
                        action = p.controls[event.key]
                        if action == "rotate":
                            p.rotate()
                        else:
                            p.move(action[0], action[1])

        for p in players:
            p.update(dt)
            p.draw(screen, font)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()