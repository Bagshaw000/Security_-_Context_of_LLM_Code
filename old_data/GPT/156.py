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
    lines_cleared = 0
    for i in range(len(board) - 1, -1, -1):
        if all(board[i]):
            del board[i]
            board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            lines_cleared += 1
    return lines_cleared

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    boards = [[[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)] for _ in range(3)]
    pieces = [Piece() for _ in range(3)]
    scores = [0, 0, 0]
    current_player = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pieces[current_player].x -= 1
            if check_collision(boards[current_player], pieces[current_player]):
                pieces[current_player].x += 1
        if keys[pygame.K_RIGHT]:
            pieces[current_player].x += 1
            if check_collision(boards[current_player], pieces[current_player]):
                pieces[current_player].x -= 1
        if keys[pygame.K_DOWN]:
            pieces[current_player].y += 1
            if check_collision(boards[current_player], pieces[current_player]):
                pieces[current_player].y -= 1
        if keys[pygame.K_UP]:
            pieces[current_player].rotate()
            if check_collision(boards[current_player], pieces[current_player]):
                pieces[current_player].rotate()  

        pieces[current_player].y += 1
        if check_collision(boards[current_player], pieces[current_player]):
            pieces[current_player].y -= 1
            merge(boards[current_player], pieces[current_player])
            clear_lines(boards[current_player])
            pieces[current_player] = Piece()

        screen.fill((0, 0, 0))
        for i in range(3):
            draw_board(screen, boards[i])
            for y, row in enumerate(pieces[i].shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, pieces[i].color, ((i * (SCREEN_WIDTH // 3)) + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()