import pygame
import random


pygame.init()


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30 


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 127, 0)
]


GRID_WIDTH = 10
GRID_HEIGHT = 20


SHAPES = [
    [[1, 1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[0, 1, 0], [1, 1, 1]], 
    [[0, 1, 1], [1, 1, 0]], 
    [[1, 1, 0], [0, 1, 1]], 
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]]  
]

class PlayerBoard:
    
    def __init__(self, x_offset):
        self.x_offset = x_offset
        
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.color = random.choice(COLORS)
        self.game_over = False
        self.score = 0

    def new_piece(self):
        
        return random.choice(SHAPES)

    def rotate_piece(self):
        
        new_shape = [list(row) for row in zip(*self.current_piece[::-1])]
        if self.is_valid_move(new_shape, self.piece_x, self.piece_y):
            self.current_piece = new_shape

    def is_valid_move(self, shape, x, y):
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = x + col_idx
                    new_y = y + row_idx
                    
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def lock_piece(self):
        
        for row_idx, row in enumerate(self.current_piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    
                    if self.piece_y + row_idx < 0:
                        self.game_over = True
                        return
                    self.grid[self.piece_y + row_idx][self.piece_x + col_idx] = self.color
        self.clear_lines()
        self.current_piece = self.new_piece()
        self.color = random.choice(COLORS)
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        
        if not self.is_valid_move(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True

    def clear_lines(self):
        
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        self.score += lines_cleared * 100
        
        for _ in range(lines_cleared):
            new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        self.grid = new_grid

    def update(self):
        
        if self.game_over:
            return
        if self.is_valid_move(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            self.lock_piece()

    def move(self, dx):
        
        if not self.game_over and self.is_valid_move(self.current_piece, self.piece_x + dx, self.piece_y):
            self.piece_x += dx

    def drop(self):
        
        if not self.game_over and self.is_valid_move(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1

    def draw(self, screen):
        
        
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (self.x_offset + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        
        if not self.game_over:
            for row_idx, row in enumerate(self.current_piece):
                for col_idx, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.color, (self.x_offset + (self.piece_x + col_idx) * BLOCK_SIZE, (self.piece_y + row_idx) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        
        pygame.draw.rect(screen, WHITE, (self.x_offset, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 2)

def main():
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3-Player Block Stacker")
    clock = pygame.time.Clock()
    
    
    
    players = [
        PlayerBoard(50),
        PlayerBoard(325),
        PlayerBoard(600)
    ]

    fall_time = 0
    fall_speed = 500 
    run = True

    while run:
        
        dt = clock.tick(60) 
        fall_time += dt

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_w: players[0].rotate_piece()
                if event.key == pygame.K_a: players[0].move(-1)
                if event.key == pygame.K_d: players[0].move(1)
                if event.key == pygame.K_s: players[0].drop()

                
                if event.key == pygame.K_UP: players[1].rotate_piece()
                if event.key == pygame.K_LEFT: players[1].move(-1)
                if event.key == pygame.K_RIGHT: players[1].move(1)
                if event.key == pygame.K_DOWN: players[1].drop()

                
                if event.key == pygame.K_i: players[2].rotate_piece()
                if event.key == pygame.K_j: players[2].move(-1)
                if event.key == pygame.K_l: players[2].move(1)
                if event.key == pygame.K_k: players[2].drop()

        
        if fall_time > fall_speed:
            for p in players:
                p.update()
            fall_time = 0

        
        screen.fill(BLACK)

        
        font = pygame.font.SysFont('Arial', 24)
        for i, p in enumerate(players):
            p.draw(screen)
            
            score_text = font.render(f"P{i+1} Score: {p.score}", True, WHITE)
            screen.blit(score_text, (p.x_offset, SCREEN_HEIGHT - 50))
            if p.game_over:
                over_text = font.render("GAME OVER", True, (255, 0, 0))
                screen.blit(over_text, (p.x_offset + 20, SCREEN_HEIGHT // 2))

        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    
    try:
        main()
    except Exception as e:
        
        print(f"The game encountered an error and closed safely: {e}")
        pygame.quit()