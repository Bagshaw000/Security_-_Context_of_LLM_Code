import pygame
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20


COLORS = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 134, 22),
]

SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [6, 7, 10, 11]],
    [[6, 7, 9, 10], [5, 6, 10, 11]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def image(self):
        return SHAPES[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])

class TetrisEngine:
    def __init__(self, height, width, x_offset):
        self.height = height
        self.width = width
        self.x_offset = x_offset
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.state = "start"
        self.piece = None

    def new_piece(self):
        self.piece = Piece(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.piece.image():
                    if i + self.piece.y > self.height - 1 or \
                       j + self.piece.x > self.width - 1 or \
                       j + self.piece.x < 0 or \
                       self.field[i + self.piece.y][j + self.piece.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.piece.y += 1
        self.piece.y -= 1
        self.freeze()

    def go_down(self):
        self.piece.y += 1
        if self.intersects():
            self.piece.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.piece.image():
                    self.field[i + self.piece.y][j + self.piece.x] = self.piece.color
        self.break_lines()
        self.new_piece()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.piece.x
        self.piece.x += dx
        if self.intersects():
            self.piece.x = old_x

    def rotate(self):
        old_rotation = self.piece.rotation
        self.piece.rotate()
        if self.intersects():
            self.piece.rotation = old_rotation

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brad's 3-Player Distributed Tetris Architecture")
    clock = pygame.time.Clock()
    fps = 25

    
    p1 = TetrisEngine(BOARD_HEIGHT, BOARD_WIDTH, 50)
    p2 = TetrisEngine(BOARD_HEIGHT, BOARD_WIDTH, 450)
    p3 = TetrisEngine(BOARD_HEIGHT, BOARD_WIDTH, 850)
    players = [p1, p2, p3]

    for p in players:
        p.new_piece()

    counter = 0
    done = False

    while not done:
        if any(p.piece is None for p in players):
            for p in players:
                if p.piece is None: p.new_piece()

        counter += 1
        if counter > 100000: counter = 0

        if counter % (fps // 2) == 0:
            for p in players:
                if p.state == "start":
                    p.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                
                if p1.state == "start":
                    if event.key == pygame.K_w: p1.rotate()
                    if event.key == pygame.K_s: p1.go_down()
                    if event.key == pygame.K_a: p1.go_side(-1)
                    if event.key == pygame.K_d: p1.go_side(1)
                    if event.key == pygame.K_q: p1.go_space()
                
                if p2.state == "start":
                    if event.key == pygame.K_i: p2.rotate()
                    if event.key == pygame.K_k: p2.go_down()
                    if event.key == pygame.K_j: p2.go_side(-1)
                    if event.key == pygame.K_l: p2.go_side(1)
                    if event.key == pygame.K_u: p2.go_space()
                
                if p3.state == "start":
                    if event.key == pygame.K_UP: p3.rotate()
                    if event.key == pygame.K_DOWN: p3.go_down()
                    if event.key == pygame.K_LEFT: p3.go_side(-1)
                    if event.key == pygame.K_RIGHT: p3.go_side(1)
                    if event.key == pygame.K_RSHIFT: p3.go_space()
                
                
                if event.key == pygame.K_ESCAPE:
                    for p in players:
                        p.__init__(BOARD_HEIGHT, BOARD_WIDTH, p.x_offset)
                        p.new_piece()

        screen.fill((40, 44, 52))

        for p_idx, p in enumerate(players):
            
            pygame.draw.rect(screen, (128, 128, 128), [p.x_offset - 1, 0, p.width * BLOCK_SIZE + 2, p.height * BLOCK_SIZE + 2], 1)
            
            
            for y in range(p.height):
                for x in range(p.width):
                    pygame.draw.rect(screen, (60, 60, 60), [p.x_offset + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)
                    if p.field[y][x] > 0:
                        pygame.draw.rect(screen, COLORS[p.field[y][x]], [p.x_offset + x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2])

            
            if p.piece is not None:
                for i in range(4):
                    for j in range(4):
                        p_val = i * 4 + j
                        if p_val in p.piece.image():
                            pygame.draw.rect(screen, COLORS[p.piece.color],
                                             [p.x_offset + (j + p.piece.x) * BLOCK_SIZE + 1,
                                              (i + p.piece.y) * BLOCK_SIZE + 1,
                                              BLOCK_SIZE - 2, BLOCK_SIZE - 2])

            
            font = pygame.font.SysFont('Calibri', 25, True, False)
            label = font.render(f"P{p_idx+1} Score: {p.score}", True, (255, 255, 255))
            screen.blit(label, [p.x_offset, 620])
            
            if p.state == "gameover":
                go_label = font.render("GAME OVER", True, (255, 0, 0))
                screen.blit(go_label, [p.x_offset, 300])

        
        info_font = pygame.font.SysFont('Arial', 14, False, False)
        screen.blit(info_font.render("P1: WASD | P2: IJKL | P3: ARROWS", True, (200, 200, 200)), [20, 660])
        screen.blit(info_font.render("ESC to Reset", True, (200, 200, 200)), [1100, 660])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()