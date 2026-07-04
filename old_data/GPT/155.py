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

    def valid_move(self, dx, dy):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_pos[1] + x + dx
                    new_y = self.current_pos[0] + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or self.grid[new_y][new_x]:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_pos[0] + y][self.current_pos[1] + x] = 1
        self.clear_lines()
        self.current_piece = self.new_piece()
        self.current_pos = [0, GRID_WIDTH // 2 - 1]

    def clear_lines(self):
        self.grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        while len(self.grid) < GRID_HEIGHT:
            self.grid.insert(0, [0] * GRID_WIDTH)

    def drop_piece(self):
        if self.valid_move(1, 0):
            self.current_pos[0] += 1
        else:
            self.lock_piece()

    def move_piece(self, dx):
        if self.valid_move(0, dx):
            self.current_pos[1] += dx


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    tetris = Tetris()
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(-1)
                if event.key == pygame.K_RIGHT:
                    tetris.move_piece(1)
                if event.key == pygame.K_DOWN:
                    tetris.drop_piece()
                if event.key == pygame.K_UP:
                    tetris.rotate_piece()

        tetris.drop_piece()

        for y, row in enumerate(tetris.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[cell], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for y, row in enumerate(tetris.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[1], ((tetris.current_pos[1] + x) * BLOCK_SIZE, (tetris.current_pos[0] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()