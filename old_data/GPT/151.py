import pygame
import random


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE


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
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 1

    def drop_piece(self):
        if self.valid_move(1, 0):
            self.current_pos[0] += 1
        else:
            self.lock_piece()

    def move_piece(self, dx):
        if self.valid_move(0, dx):
            self.current_pos[1] += dx

    def get_grid(self):
        grid_copy = [row[:] for row in self.grid]
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    grid_copy[self.current_pos[0] + y][self.current_pos[1] + x] = 1
        return grid_copy

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLORS[cell]
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

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
        for i, game in enumerate(games):
            if keys[pygame.K_LEFT + i * 2]:
                game.move_piece(-1)
            if keys[pygame.K_RIGHT + i * 2]:
                game.move_piece(1)
            if keys[pygame.K_DOWN + i * 2]:
                game.drop_piece()
            if keys[pygame.K_UP + i * 2]:
                game.rotate_piece()

        for game in games:
            game.drop_piece()

        screen.fill((0, 0, 0))
        for i, game in enumerate(games):
            draw_grid(screen, game.get_grid())
            pygame.draw.rect(screen, (255, 255, 255), (i * SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()