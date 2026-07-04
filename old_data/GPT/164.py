import pygame
import random


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
        return random.choice(SHAPES)

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
        lines_to_clear = [i for i in range(GRID_HEIGHT) if all(self.grid[i])]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 1

    def drop_piece(self):
        if self.valid_move(0, 1):
            self.current_pos[0] += 1
        else:
            self.lock_piece()

    def move_piece(self, dx):
        if self.valid_move(dx, 0):
            self.current_pos[1] += dx

    def get_grid(self):
        grid_copy = [row[:] for row in self.grid]
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    grid_copy[self.current_pos[0] + i][self.current_pos[1] + j] = 1
        return grid_copy

def draw_grid(screen, grid):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            color = COLORS[val]
            pygame.draw.rect(screen, color, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH * 3, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    games = [Tetris() for _ in range(3)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: games[0].move_piece(-1)
        if keys[pygame.K_RIGHT]: games[0].move_piece(1)
        if keys[pygame.K_DOWN]: games[0].drop_piece()
        if keys[pygame.K_UP]: games[0].rotate_piece()

        if keys[pygame.K_a]: games[1].move_piece(-1)
        if keys[pygame.K_d]: games[1].move_piece(1)
        if keys[pygame.K_s]: games[1].drop_piece()
        if keys[pygame.K_w]: games[1].rotate_piece()

        if keys[pygame.K_j]: games[2].move_piece(-1)
        if keys[pygame.K_l]: games[2].move_piece(1)
        if keys[pygame.K_k]: games[2].drop_piece()
        if keys[pygame.K_i]: games[2].rotate_piece()

        for game in games:
            game.drop_piece()

        screen.fill((0, 0, 0))
        for idx, game in enumerate(games):
            draw_grid(screen, game.get_grid())
            pygame.draw.rect(screen, (255, 255, 255), (idx * SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()