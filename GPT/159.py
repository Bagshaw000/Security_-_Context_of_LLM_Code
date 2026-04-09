import pygame
import random


pygame.init()


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

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(board, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                if (x + piece.x < 0 or x + piece.x >= len(board[0]) or
                        y + piece.y >= len(board) or
                        board[y + piece.y][x + piece.x]):
                    return True
    return False

def merge(board, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + piece.y][x + piece.x] = piece.color

def clear_lines(board):
    lines = 0
    for i, row in enumerate(board):
        if all(row):
            del board[i]
            board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            lines += 1
    return lines

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH * 3, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    boards = [[[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)] for _ in range(3)]
    pieces = [Piece() for _ in range(3)]
    scores = [0, 0, 0]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in range(3):
            piece = pieces[i]
            if not check_collision(boards[i], piece):
                piece.y += 1
            else:
                merge(boards[i], piece)
                scores[i] += clear_lines(boards[i])
                pieces[i] = Piece()

        screen.fill((0, 0, 0))
        for i in range(3):
            draw_board(screen, boards[i])
            piece = pieces[i]
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, piece.color, ((i * SCREEN_WIDTH) + (x + piece.x) * BLOCK_SIZE, (y + piece.y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()