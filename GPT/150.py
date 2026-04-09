import pygame
import random


pygame.init()


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 10


COLORS = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)
]


SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]]   
]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.current_pos = [0, GRID_WIDTH // 2 - 1]
    
    def new_piece(self):
        shape = random.choice(SHAPES)
        return shape

    def rotate_piece(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]

    def valid_move(self, offset):
        for i, row in enumerate(self.current_piece):
            for j, block in enumerate(row):
                if block:
                    x = self.current_pos[0] + i + offset[0]
                    y = self.current_pos[1] + j + offset[1]
                    if x < 0 or x >= GRID_HEIGHT or y < 0 or y >= GRID_WIDTH or self.grid[x][y]:
                        return False
        return True

    def merge_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, block in enumerate(row):
                if block:
                    self.grid[self.current_pos[0] + i][self.current_pos[1] + j] = 1

    def clear_lines(self):
        self.grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        while len(self.grid) < GRID_HEIGHT:
            self.grid.insert(0, [0] * GRID_WIDTH)

def draw_grid(screen, grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            color = COLORS[cell]
            pygame.draw.rect(screen, color, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    tetris = Tetris()
    running = True

    while running:
        screen.fill((0, 0, 0))
        draw_grid(screen, tetris.grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tetris.valid_move((0, -1)):
                    tetris.current_pos[1] -= 1
                if event.key == pygame.K_RIGHT and tetris.valid_move((0, 1)):
                    tetris.current_pos[1] += 1
                if event.key == pygame.K_DOWN and tetris.valid_move((1, 0)):
                    tetris.current_pos[0] += 1
                if event.key == pygame.K_UP:
                    tetris.rotate_piece()
                    if not tetris.valid_move((0, 0)):
                        tetris.rotate_piece()  

        if tetris.valid_move((1, 0)):
            tetris.current_pos[0] += 1
        else:
            tetris.merge_piece()
            tetris.clear_lines()
            tetris.current_piece = tetris.new_piece()
            tetris.current_pos = [0, GRID_WIDTH // 2 - 1]

        draw_grid(screen, tetris.grid)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()