import pygame
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
BLOCK_SIZE = 30
FPS = 60


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
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
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def get_image(self):
        return self.shape

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisEngine:
    def __init__(self, x_offset, player_name):
        self.x_offset = x_offset
        self.player_name = player_name
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.5 

    def new_piece(self):
        shape = random.choice(SHAPES)
        return Tetromino(self.width // 2 - len(shape[0]) // 2, 0, shape)

    def valid_move(self, piece, adj_x=0, adj_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + adj_x
                    new_y = piece.y + y + adj_y
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if self.current_piece.y + y < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [BLACK for _ in range(self.width)])
        self.score += len(lines_to_clear) ** 2 * 100

    def update(self, dt):
        if self.game_over:
            return
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if self.valid_move(self.current_piece, adj_y=1):
                self.current_piece.y += 1
            else:
                self.lock_piece()
            self.fall_time = 0

    def move(self, dx):
        if not self.game_over and self.valid_move(self.current_piece, adj_x=dx):
            self.current_piece.x += dx

    def rotate(self):
        if self.game_over:
            return
        old_shape = self.current_piece.shape
        self.current_piece.rotate()
        if not self.valid_move(self.current_piece):
            self.current_piece.shape = old_shape

    def drop(self):
        if not self.game_over:
            while self.valid_move(self.current_piece, adj_y=1):
                self.current_piece.y += 1
            self.lock_piece()

    def draw(self, surface):
        
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(surface, self.grid[y][x], 
                                 (self.x_offset + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, GRAY, 
                                 (self.x_offset + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        
        if not self.game_over:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(surface, self.current_piece.color,
                                         (self.x_offset + (self.current_piece.x + x) * BLOCK_SIZE, 
                                          (self.current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        
        font = pygame.font.SysFont('Arial', 24)
        name_label = font.render(self.player_name, True, WHITE)
        score_label = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(name_label, (self.x_offset, self.height * BLOCK_SIZE + 10))
        surface.blit(score_label, (self.x_offset, self.height * BLOCK_SIZE + 40))
        if self.game_over:
            over_label = font.render("GAME OVER", True, (255, 0, 0))
            surface.blit(over_label, (self.x_offset + 20, self.height * BLOCK_SIZE // 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Amazon Multi-Player Tetris (3 Players)")
    clock = pygame.time.Clock()

    
    
    
    p1 = TetrisEngine(50, "Player 1 (WASD)")
    p2 = TetrisEngine(450, "Player 2 (Arrows)")
    p3 = TetrisEngine(850, "Player 3 (IJKL)")
    players = [p1, p2, p3]

    running = True
    while running:
        dt = clock.get_rawtime() / 1000.0
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_a: p1.move(-1)
                if event.key == pygame.K_d: p1.move(1)
                if event.key == pygame.K_s: p1.drop()
                if event.key == pygame.K_w: p1.rotate()
                
                
                if event.key == pygame.K_LEFT: p2.move(-1)
                if event.key == pygame.K_RIGHT: p2.move(1)
                if event.key == pygame.K_DOWN: p2.drop()
                if event.key == pygame.K_UP: p2.rotate()

                
                if event.key == pygame.K_j: p3.move(-1)
                if event.key == pygame.K_l: p3.move(1)
                if event.key == pygame.K_k: p3.drop()
                if event.key == pygame.K_i: p3.rotate()

        screen.fill(BLACK)
        
        for p in players:
            p.update(dt)
            p.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    main()