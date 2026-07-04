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
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        return shape

    def rotate_piece(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]

    def valid_move(self, dx, dy):
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    x, y = self.current_pos[0] + i + dy, self.current_pos[1] + j + dx
                    if x < 0 or x >= GRID_HEIGHT or y < 0 or y >= GRID_WIDTH or self.grid[x][y]:
                        return False
        return True

    def lock_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    self.grid[self.current_pos[0] + i][self.current_pos[1] + j] = 1
        self.clear_lines()
        self.current_piece = self.new_piece()
        self.current_pos = [0, GRID_WIDTH // 2 - 1]

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 1

    def drop(self):
        if self.valid_move(0, 1):
            self.current_pos[0] += 1
        else:
            self.lock_piece()

    def move(self, dx):
        if self.valid_move(dx, 0):
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
                    tetris.move(-1)
                if event.key == pygame.K_RIGHT:
                    tetris.move(1)
                if event.key == pygame.K_DOWN:
                    tetris.drop()
                if event.key == pygame.K_UP:
                    tetris.rotate_piece()

        tetris.drop()
        for i, row in enumerate(tetris.grid):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, COLORS[val], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for i, row in enumerate(tetris.current_piece):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, COLORS[val], ((tetris.current_pos[1] + j) * BLOCK_SIZE, (tetris.current_pos[0] + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()