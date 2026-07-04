import pygame
import random


pygame.init()


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 10


COLORS = [
    (0, 0, 0),  
    (255, 0, 0),  
    (0, 255, 0),  
    (0, 0, 255),  
    (255, 255, 0),  
    (255, 165, 0),  
    (128, 0, 128)   
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
        self.board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.randint(1, len(COLORS) - 1)
        return (shape, color)

    def rotate_piece(self):
        self.current_piece[0] = [list(row) for row in zip(*self.current_piece[0][::-1])]

    def drop_piece(self):
        
        pass

    def clear_lines(self):
        
        pass

    def draw_board(self, screen):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                pygame.draw.rect(screen, COLORS[self.board[y][x]], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Three-Player Tetris")
    clock = pygame.time.Clock()
    game = Tetris()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  
        game.draw_board(screen)
        pygame.display.flip()  
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()