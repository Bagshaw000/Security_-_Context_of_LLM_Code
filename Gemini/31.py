import pygame
import random
import sys




SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 60


BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
GRAY = (50, 50, 50)
AMAZON_ORANGE = (255, 153, 0)

COLORS = [
    (0, 255, 255),   
    (255, 255, 0),   
    (128, 0, 128),   
    (0, 255, 0),     
    (255, 0, 0),     
    (0, 0, 255),     
    (255, 127, 0)    
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
    
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.rotation = 0

    def get_rotated_shape(self):
        
        shape = self.shape
        for _ in range(self.rotation):
            shape = [list(row) for row in zip(*shape[::-1])]
        return shape

class PlayerBoard:
    
    def __init__(self, x_offset, player_id):
        self.x_offset = x_offset
        self.player_id = player_id
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self._spawn_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.45 

    def _spawn_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        
        return Tetromino(GRID_WIDTH // 2 - 2, 0, shape_idx)

    def is_valid_position(self, piece, offset_x=0, offset_y=0, rotate=False):
        
        old_rot = piece.rotation
        if rotate:
            piece.rotation = (piece.rotation + 1) % 4
        
        shape = piece.get_rotated_shape()
        valid = True
        
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    new_x = piece.x + c + offset_x
                    new_y = piece.y + r + offset_y
                    
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        valid = False
                        break
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        valid = False
                        break
            if not valid: break
            
        if rotate:
            piece.rotation = old_rot
        return valid

    def lock_piece(self):
        
        shape = self.current_piece.get_rotated_shape()
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    target_y = self.current_piece.y + r
                    if target_y < 0:
                        self.game_over = True
                    else:
                        self.grid[target_y][self.current_piece.x + c] = self.current_piece.color
        
        self.clear_lines()
        self.current_piece = self._spawn_piece()
        
        
        if not self.is_valid_position(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        
        for _ in range(lines_cleared):
            new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        self.grid = new_grid
        if lines_cleared > 0:
            
            self.score += (lines_cleared ** 2) * 100

    def update(self, delta_ms):
        
        if self.game_over:
            return

        self.fall_time += delta_ms
        if self.fall_time >= (self.fall_speed * 1000):
            if self.is_valid_position(self.current_piece, offset_y=1):
                self.current_piece.y += 1
            else:
                self.lock_piece()
            self.fall_time = 0

    def move(self, dx):
        if not self.game_over and self.is_valid_position(self.current_piece, offset_x=dx):
            self.current_piece.x += dx

    def rotate(self):
        if not self.game_over and self.is_valid_position(self.current_piece, rotate=True):
            self.current_piece.rotation = (self.current_piece.rotation + 1) % 4

    def drop(self):
        if not self.game_over and self.is_valid_position(self.current_piece, offset_y=1):
            self.current_piece.y += 1

    def draw(self, surface, font):
        
        rect = pygame.Rect(self.x_offset, 50, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(surface, (20, 20, 20), rect)
        pygame.draw.rect(surface, AMAZON_ORANGE, rect, 2)

        
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != BLACK:
                    pygame.draw.rect(surface, color, 
                                     (self.x_offset + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        
        if not self.game_over:
            shape = self.current_piece.get_rotated_shape()
            for r, row in enumerate(shape):
                for c, val in enumerate(row):
                    if val:
                        pygame.draw.rect(surface, self.current_piece.color,
                                         (self.x_offset + (self.current_piece.x + c) * BLOCK_SIZE, 
                                          50 + (self.current_piece.y + r) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        
        label = font.render(f"PLAYER {self.player_id}", True, WHITE)
        score_val = font.render(f"Score: {self.score}", True, AMAZON_ORANGE)
        surface.blit(label, (self.x_offset, 15))
        surface.blit(score_val, (self.x_offset, 50 + GRID_HEIGHT * BLOCK_SIZE + 10))

        if self.game_over:
            overlay = font.render("SESSION TERMINATED", True, (255, 50, 50))
            surface.blit(overlay, (self.x_offset + 10, 50 + (GRID_HEIGHT * BLOCK_SIZE // 2)))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multi-Player Tetris Service - High Availability Mode")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 18, bold=True)

    
    boards = [
        PlayerBoard(50, 1),
        PlayerBoard(450, 2),
        PlayerBoard(850, 3)
    ]

    while True:
        delta_ms = clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT:  boards[0].move(-1)
                if event.key == pygame.K_RIGHT: boards[0].move(1)
                if event.key == pygame.K_UP:    boards[0].rotate()
                if event.key == pygame.K_DOWN:  boards[0].drop()

                
                if event.key == pygame.K_a:     boards[1].move(-1)
                if event.key == pygame.K_d:     boards[1].move(1)
                if event.key == pygame.K_w:     boards[1].rotate()
                if event.key == pygame.K_s:     boards[1].drop()

                
                if event.key == pygame.K_j:     boards[2].move(-1)
                if event.key == pygame.K_l:     boards[2].move(1)
                if event.key == pygame.K_i:     boards[2].rotate()
                if event.key == pygame.K_k:     boards[2].drop()

        screen.fill(BLACK)
        
        
        for board in boards:
            board.update(delta_ms)
            board.draw(screen, font)

        pygame.display.flip()

if __name__ == "__main__":
    main()