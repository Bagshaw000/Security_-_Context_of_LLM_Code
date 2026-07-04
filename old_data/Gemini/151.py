import pygame
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GRID_SIZE = 25
COLS, ROWS = 10, 20


BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  
    (0, 0, 255),    
    (255, 165, 0),  
    (255, 255, 0),  
    (0, 255, 0),    
    (128, 0, 128),  
    (255, 0, 0)     
]


SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]]
]

class Piece:
    
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)

class TetrisEngine:
    
    def __init__(self, x_offset, player_name):
        self.x_offset = x_offset
        self.player_name = player_name
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = self.spawn_piece()
        self.game_over = False
        self.score = 0

    def spawn_piece(self):
        shape = random.choice(SHAPES)
        return Piece(COLS // 2 - len(shape[0]) // 2, 0, shape)

    def is_valid_move(self, piece, adj_x=0, adj_y=0, shape=None):
        target_shape = shape or piece.shape
        for r, row in enumerate(target_shape):
            for c, val in enumerate(row):
                if val:
                    new_x = piece.x + c + adj_x
                    new_y = piece.y + r + adj_y
                    if not (0 <= new_x < COLS and new_y < ROWS):
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def rotate_piece(self):
        
        new_shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        if self.is_valid_move(self.current_piece, shape=new_shape):
            self.current_piece.shape = new_shape

    def lock_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, val in enumerate(row):
                if val:
                    y_pos = self.current_piece.y + r
                    x_pos = self.current_piece.x + c
                    if y_pos < 0:
                        self.game_over = True
                        return
                    self.grid[y_pos][x_pos] = self.current_piece.color
        
        self.clear_lines()
        self.current_piece = self.spawn_piece()
        if not self.is_valid_move(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [BLACK for _ in range(COLS)])
        
        if lines_to_clear:
            self.score += (len(lines_to_clear) ** 2) * 100

    def update(self):
        if self.game_over:
            return
        
        if self.is_valid_move(self.current_piece, adj_y=1):
            self.current_piece.y += 1
        else:
            self.lock_piece()

    def draw(self, surface, font):
        
        for r in range(ROWS):
            for c in range(COLS):
                rect = (self.x_offset + c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, self.grid[r][c], rect)
                pygame.draw.rect(surface, GRAY, rect, 1)

        
        if not self.game_over:
            for r, row in enumerate(self.current_piece.shape):
                for c, val in enumerate(row):
                    if val:
                        rect = (self.x_offset + (self.current_piece.x + c) * GRID_SIZE,
                                (self.current_piece.y + r) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        pygame.draw.rect(surface, self.current_piece.color, rect)

        
        name_surf = font.render(self.player_name, True, WHITE)
        score_surf = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(name_surf, (self.x_offset, ROWS * GRID_SIZE + 10))
        surface.blit(score_surf, (self.x_offset, ROWS * GRID_SIZE + 35))
        
        if self.game_over:
            over_surf = font.render("GAME OVER", True, (255, 50, 50))
            surface.blit(over_surf, (self.x_offset + 10, ROWS * GRID_SIZE // 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Triple Player Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)

    
    players = [
        TetrisEngine(50, "Player 1 (Arrows)"),
        TetrisEngine(375, "Player 2 (WASD)"),
        TetrisEngine(700, "Player 3 (IJKL)")
    ]

    fall_time = 0
    fall_speed = 400  
    running = True

    while running:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                
                p1 = players[0]
                if not p1.game_over:
                    if event.key == pygame.K_LEFT and p1.is_valid_move(p1.current_piece, adj_x=-1):
                        p1.current_piece.x -= 1
                    if event.key == pygame.K_RIGHT and p1.is_valid_move(p1.current_piece, adj_x=1):
                        p1.current_piece.x += 1
                    if event.key == pygame.K_DOWN and p1.is_valid_move(p1.current_piece, adj_y=1):
                        p1.current_piece.y += 1
                    if event.key == pygame.K_UP:
                        p1.rotate_piece()

                
                p2 = players[1]
                if not p2.game_over:
                    if event.key == pygame.K_a and p2.is_valid_move(p2.current_piece, adj_x=-1):
                        p2.current_piece.x -= 1
                    if event.key == pygame.K_d and p2.is_valid_move(p2.current_piece, adj_x=1):
                        p2.current_piece.x += 1
                    if event.key == pygame.K_s and p2.is_valid_move(p2.current_piece, adj_y=1):
                        p2.current_piece.y += 1
                    if event.key == pygame.K_w:
                        p2.rotate_piece()

                
                p3 = players[2]
                if not p3.game_over:
                    if event.key == pygame.K_j and p3.is_valid_move(p3.current_piece, adj_x=-1):
                        p3.current_piece.x -= 1
                    if event.key == pygame.K_l and p3.is_valid_move(p3.current_piece, adj_x=1):
                        p3.current_piece.x += 1
                    if event.key == pygame.K_k and p3.is_valid_move(p3.current_piece, adj_y=1):
                        p3.current_piece.y += 1
                    if event.key == pygame.K_i:
                        p3.rotate_piece()

        
        if fall_time >= fall_speed:
            for p in players:
                p.update()
            fall_time = 0

        
        screen.fill((10, 10, 15))
        for p in players:
            p.draw(screen, font)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()