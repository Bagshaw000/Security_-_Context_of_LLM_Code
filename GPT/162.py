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

    def merge_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_pos[0] + y][self.current_pos[1] + x] = 1
        self.clear_lines()

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
            self.merge_piece()
            self.current_piece = self.new_piece()
            self.current_pos = [0, GRID_WIDTH // 2 - 1]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH * 3, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.games = [Tetris() for _ in range(3)]
        self.running = True

    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                color = COLORS[self.games[0].grid[i][j]]
                pygame.draw.rect(self.screen, color, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for idx, game in enumerate(self.games):
            self.draw_grid()
            for y, row in enumerate(game.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        color = COLORS[1]
                        pygame.draw.rect(self.screen, color, ((game.current_pos[1] + x + idx * GRID_WIDTH) * BLOCK_SIZE, (game.current_pos[0] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for game in self.games:
                            if game.valid_move(0, -1):
                                game.current_pos[1] -= 1
                    if event.key == pygame.K_RIGHT:
                        for game in self.games:
                            if game.valid_move(0, 1):
                                game.current_pos[1] += 1
                    if event.key == pygame.K_DOWN:
                        for game in self.games:
                            game.drop_piece()
                    if event.key == pygame.K_UP:
                        for game in self.games:
                            game.rotate_piece()

            for game in self.games:
                game.drop_piece()
            self.draw()
            self.clock.tick(10)

if __name__ == "__main__":
    Game().run()