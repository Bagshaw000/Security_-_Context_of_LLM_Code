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

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Game:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_tetromino = Tetromino()
        self.score = 0

    def draw_grid(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[self.grid[y][x]]
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def draw_tetromino(self, screen):
        for y, row in enumerate(self.current_tetromino.shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, self.current_tetromino.color,
                                     ((self.current_tetromino.x + x) * BLOCK_SIZE,
                                      (self.current_tetromino.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

    def check_collision(self):
        for y, row in enumerate(self.current_tetromino.shape):
            for x, value in enumerate(row):
                if value:
                    if (self.current_tetromino.x + x < 0 or
                        self.current_tetromino.x + x >= GRID_WIDTH or
                        self.current_tetromino.y + y >= GRID_HEIGHT or
                        self.grid[self.current_tetromino.y + y][self.current_tetromino.x + x]):
                        return True
        return False

    def merge_tetromino(self):
        for y, row in enumerate(self.current_tetromino.shape):
            for x, value in enumerate(row):
                if value:
                    self.grid[self.current_tetromino.y + y][self.current_tetromino.x + x] = COLORS.index(self.current_tetromino.color)

    def clear_lines(self):
        lines_to_clear = [i for i in range(GRID_HEIGHT) if all(self.grid[i])]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 1

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        screen.fill((0, 0, 0))
        game.draw_grid(screen)
        game.draw_tetromino(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.current_tetromino.y += 1
        if game.check_collision():
            game.current_tetromino.y -= 1
            game.merge_tetromino()
            game.clear_lines()
            game.current_tetromino = Tetromino()
            if game.check_collision():
                running = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()