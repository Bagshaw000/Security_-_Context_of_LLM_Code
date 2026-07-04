import pygame
import random


pygame.init()


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 10


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]


SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
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
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    pieces = [Piece() for _ in range(3)]
    current_piece = pieces[0]
    player_index = 0

    while True:
        screen.fill(BLACK)
        draw_board(screen, board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_piece.x -= 1
        if keys[pygame.K_RIGHT]:
            current_piece.x += 1
        if keys[pygame.K_DOWN]:
            current_piece.y += 1
        if keys[pygame.K_UP]:
            current_piece.rotate()

        
        for y, row in enumerate(current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, current_piece.color, ((current_piece.x + x) * BLOCK_SIZE, (current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()