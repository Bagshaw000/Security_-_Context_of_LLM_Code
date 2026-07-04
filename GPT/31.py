import pygame
import random


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
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
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_tetromino = Tetromino()
        self.score = 0

    def collide(self):
        for y, row in enumerate(self.current_tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (self.current_tetromino.x + x < 0 or
                        self.current_tetromino.x + x >= len(self.board[0]) or
                        self.current_tetromino.y + y >= len(self.board) or
                        self.board[self.current_tetromino.y + y][self.current_tetromino.x + x]):
                        return True
        return False

    def merge(self):
        for y, row in enumerate(self.current_tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_tetromino.y + y][self.current_tetromino.x + x] = self.current_tetromino.color

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            self.score += 100

    def drop(self):
        self.current_tetromino.y += 1
        if self.collide():
            self.current_tetromino.y -= 1
            self.merge()
            self.clear_lines()
            self.current_tetromino = Tetromino()
            if self.collide():
                return False
        return True

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    tetris = Tetris()
    running = True

    while running:
        screen.fill((0, 0, 0))
        draw_board(screen, tetris.board)
        draw_board(screen, tetris.current_tetromino.shape)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        tetris.drop()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()