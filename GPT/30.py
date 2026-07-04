import pygame
import random


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // GRID_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


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
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    def valid_position(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (x + tetromino.x < 0 or x + tetromino.x >= BOARD_WIDTH or
                            y + tetromino.y >= BOARD_HEIGHT or
                            self.grid[y + tetromino.y][x + tetromino.x]):
                        return False
        return True

    def merge(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + tetromino.y][x + tetromino.x] = tetromino.color

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * BOARD_WIDTH)

class Game:
    def __init__(self):
        self.board = Board()
        self.tetromino = Tetromino()
        self.score = 0

    def drop(self):
        self.tetromino.y += 1
        if not self.board.valid_position(self.tetromino):
            self.tetromino.y -= 1
            self.board.merge(self.tetromino)
            self.board.clear_lines()
            self.tetromino = Tetromino()

    def rotate(self):
        self.tetromino.rotate()
        if not self.board.valid_position(self.tetromino):
            self.tetromino.rotate()  

def draw_board(screen, board):
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        screen.fill((0, 0, 0))
        game.drop()
        draw_board(screen, game.board)
        draw_board(screen, game.tetromino)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.tetromino.x -= 1
                    if not game.board.valid_position(game.tetromino):
                        game.tetromino.x += 1
                if event.key == pygame.K_RIGHT:
                    game.tetromino.x += 1
                    if not game.board.valid_position(game.tetromino):
                        game.tetromino.x -= 1
                if event.key == pygame.K_DOWN:
                    game.drop()
                if event.key == pygame.K_UP:
                    game.rotate()

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()