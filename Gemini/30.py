import pygame
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30


WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),  
    (255, 255, 0),  
    (128, 0, 128),  
    (0, 255, 0),    
    (255, 0, 0),    
    (0, 0, 255),    
    (255, 165, 0)   
]


S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
I = [['..0..', '..0..', '..0..', '..0..', '.....'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

SHAPES = [S, Z, I, O, J, L, T]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

class TetrisGame:
    def __init__(self, x_offset, player_name):
        self.x_offset = x_offset
        self.player_name = player_name
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.locked_positions = {}  
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.game_over = False
        self.score = 0

    def get_shape(self):
        return Piece(5, 0, random.choice(SHAPES))

    def convert_shape_format(self, piece):
        positions = []
        format = piece.shape[piece.rotation % len(piece.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((piece.x + j - 2, piece.y + i - 4))
        return positions

    def valid_space(self, piece):
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format(piece)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self):
        for pos in self.locked_positions:
            x, y = pos
            if y < 0:
                return True
        return False

    def clear_rows(self):
        inc = 0
        for i in range(len(self.grid)-1, -1, -1):
            row = self.grid[i]
            if BLACK not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(self.locked_positions.keys()), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
        return inc

    def update_grid(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.locked_positions:
                    c = self.locked_positions[(j, i)]
                    self.grid[i][j] = c

    def draw(self, surface):
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(surface, self.grid[i][j], (self.x_offset + j*BLOCK_SIZE, 100 + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        
        pygame.draw.rect(surface, WHITE, (self.x_offset, 100, GRID_WIDTH*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE), 2)
        
        
        font = pygame.font.SysFont('Arial', 30)
        label = font.render(f"{self.player_name}: {self.score}", 1, WHITE)
        surface.blit(label, (self.x_offset + (GRID_WIDTH*BLOCK_SIZE/2 - label.get_width()/2), 50))

        if self.game_over:
            lost_label = font.render("GAME OVER", 1, (255, 0, 0))
            surface.blit(lost_label, (self.x_offset + (GRID_WIDTH*BLOCK_SIZE/2 - lost_label.get_width()/2), 300))

def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3-Player Tetris - Junior Dev Project")
    
    
    games = [
        TetrisGame(50, "Player 1"),
        TetrisGame(450, "Player 2"),
        TetrisGame(850, "Player 3")
    ]

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    run = True

    while run:
        win.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            for g in games:
                if not g.game_over:
                    g.current_piece.y += 1
                    if not g.valid_space(g.current_piece) and g.current_piece.y > 0:
                        g.current_piece.y -= 1
                        
                        for pos in g.convert_shape_format(g.current_piece):
                            g.locked_positions[pos] = g.current_piece.color
                        g.current_piece = g.next_piece
                        g.next_piece = g.get_shape()
                        g.score += g.clear_rows() * 10
                        if g.check_lost():
                            g.game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                
                if not games[0].game_over:
                    if event.key == pygame.K_a:
                        games[0].current_piece.x -= 1
                        if not games[0].valid_space(games[0].current_piece): games[0].current_piece.x += 1
                    if event.key == pygame.K_d:
                        games[0].current_piece.x += 1
                        if not games[0].valid_space(games[0].current_piece): games[0].current_piece.x -= 1
                    if event.key == pygame.K_s:
                        games[0].current_piece.y += 1
                        if not games[0].valid_space(games[0].current_piece): games[0].current_piece.y -= 1
                    if event.key == pygame.K_w:
                        games[0].current_piece.rotation += 1
                        if not games[0].valid_space(games[0].current_piece): games[0].current_piece.rotation -= 1

                
                if not games[1].game_over:
                    if event.key == pygame.K_j:
                        games[1].current_piece.x -= 1
                        if not games[1].valid_space(games[1].current_piece): games[1].current_piece.x += 1
                    if event.key == pygame.K_l:
                        games[1].current_piece.x += 1
                        if not games[1].valid_space(games[1].current_piece): games[1].current_piece.x -= 1
                    if event.key == pygame.K_k:
                        games[1].current_piece.y += 1
                        if not games[1].valid_space(games[1].current_piece): games[1].current_piece.y -= 1
                    if event.key == pygame.K_i:
                        games[1].current_piece.rotation += 1
                        if not games[1].valid_space(games[1].current_piece): games[1].current_piece.rotation -= 1

                
                if not games[2].game_over:
                    if event.key == pygame.K_LEFT:
                        games[2].current_piece.x -= 1
                        if not games[2].valid_space(games[2].current_piece): games[2].current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        games[2].current_piece.x += 1
                        if not games[2].valid_space(games[2].current_piece): games[2].current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        games[2].current_piece.y += 1
                        if not games[2].valid_space(games[2].current_piece): games[2].current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        games[2].current_piece.rotation += 1
                        if not games[2].valid_space(games[2].current_piece): games[2].current_piece.rotation -= 1

        
        for g in games:
            g.update_grid()
            
            if not g.game_over:
                piece_pos = g.convert_shape_format(g.current_piece)
                for pos in piece_pos:
                    x, y = pos
                    if y > -1:
                        pygame.draw.rect(win, g.current_piece.color, (g.x_offset + x*BLOCK_SIZE, 100 + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            g.draw(win)

        pygame.display.update()

if __name__ == "__main__":
    main()