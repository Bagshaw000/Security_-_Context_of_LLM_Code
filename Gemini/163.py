import pygame
import random







pygame.font.init()


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 750
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20


WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128), 
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]



S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '...0.', '..00.', '..0..', '.....']]
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
        self.color = random.choice(COLORS)
        self.rotation = 0

class TetrisGame:
    def __init__(self, x_offset, player_name):
        self.x_offset = x_offset
        self.player_name = player_name
        self.grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.locked_positions = {}
        self.current_piece = Piece(5, 0, random.choice(SHAPES))
        self.next_piece = Piece(5, 0, random.choice(SHAPES))
        self.game_over = False
        self.score = 0

    def create_grid(self):
        grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if (x, y) in self.locked_positions:
                    grid[y][x] = self.locked_positions[(x, y)]
        return grid

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
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == (0,0,0)] for i in range(GRID_HEIGHT)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format(piece)
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def clear_rows(self):
        inc = 0
        for i in range(len(self.grid)-1, -1, -1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
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
        self.score += inc * 10

    def draw(self, surface):
        
        top_left_x = self.x_offset
        top_left_y = SCREEN_HEIGHT - (GRID_HEIGHT * BLOCK_SIZE) - 50

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(surface, self.grid[i][j], (top_left_x + j*BLOCK_SIZE, top_left_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        
        for i in range(GRID_HEIGHT):
            pygame.draw.line(surface, GRAY, (top_left_x, top_left_y + i*BLOCK_SIZE), (top_left_x + GRID_WIDTH*BLOCK_SIZE, top_left_y + i*BLOCK_SIZE))
        for j in range(GRID_WIDTH):
            pygame.draw.line(surface, GRAY, (top_left_x + j*BLOCK_SIZE, top_left_y), (top_left_x + j*BLOCK_SIZE, top_left_y + GRID_HEIGHT*BLOCK_SIZE))

        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, GRID_WIDTH*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE), 4)
        
        
        font = pygame.font.SysFont('arial', 30)
        label = font.render(f"{self.player_name}", 1, WHITE)
        surface.blit(label, (top_left_x + (GRID_WIDTH*BLOCK_SIZE/2 - label.get_width()/2), top_left_y - 40))
        
        score_label = font.render(f"Score: {self.score}", 1, WHITE)
        surface.blit(score_label, (top_left_x, top_left_y + GRID_HEIGHT*BLOCK_SIZE + 10))

def main():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Three Player Tetris')
    
    
    p1 = TetrisGame(50, "Harold (Arrows)")
    p2 = TetrisGame(400, "Teacher 2 (WASD)")
    p3 = TetrisGame(750, "Teacher 3 (IJKL)")
    players = [p1, p2, p3]

    clock = pygame.time.Clock()
    fall_time = 0
    run = True

    while run:
        p1.grid = p1.create_grid()
        p2.grid = p2.create_grid()
        p3.grid = p3.create_grid()
        
        fall_speed = 0.27
        fall_time += clock.get_rawtime()
        clock.tick()

        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            for p in players:
                if not p.game_over:
                    p.current_piece.y += 1
                    if not p.valid_space(p.current_piece) and p.current_piece.y > 0:
                        p.current_piece.y -= 1
                        
                        for pos in p.convert_shape_format(p.current_piece):
                            p.locked_positions[pos] = p.current_piece.color
                        p.current_piece = p.next_piece
                        p.next_piece = Piece(5, 0, random.choice(SHAPES))
                        p.clear_rows()
                        if not p.valid_space(p.current_piece):
                            p.game_over = True

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                
                if not p1.game_over:
                    if event.key == pygame.K_LEFT:
                        p1.current_piece.x -= 1
                        if not p1.valid_space(p1.current_piece): p1.current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        p1.current_piece.x += 1
                        if not p1.valid_space(p1.current_piece): p1.current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        p1.current_piece.y += 1
                        if not p1.valid_space(p1.current_piece): p1.current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        p1.current_piece.rotation += 1
                        if not p1.valid_space(p1.current_piece): p1.current_piece.rotation -= 1

                
                if not p2.game_over:
                    if event.key == pygame.K_a:
                        p2.current_piece.x -= 1
                        if not p2.valid_space(p2.current_piece): p2.current_piece.x += 1
                    if event.key == pygame.K_d:
                        p2.current_piece.x += 1
                        if not p2.valid_space(p2.current_piece): p2.current_piece.x -= 1
                    if event.key == pygame.K_s:
                        p2.current_piece.y += 1
                        if not p2.valid_space(p2.current_piece): p2.current_piece.y -= 1
                    if event.key == pygame.K_w:
                        p2.current_piece.rotation += 1
                        if not p2.valid_space(p2.current_piece): p2.current_piece.rotation -= 1

                
                if not p3.game_over:
                    if event.key == pygame.K_j:
                        p3.current_piece.x -= 1
                        if not p3.valid_space(p3.current_piece): p3.current_piece.x += 1
                    if event.key == pygame.K_l:
                        p3.current_piece.x += 1
                        if not p3.valid_space(p3.current_piece): p3.current_piece.x -= 1
                    if event.key == pygame.K_k:
                        p3.current_piece.y += 1
                        if not p3.valid_space(p3.current_piece): p3.current_piece.y -= 1
                    if event.key == pygame.K_i:
                        p3.current_piece.rotation += 1
                        if not p3.valid_space(p3.current_piece): p3.current_piece.rotation -= 1

        win.fill(BLACK)
        
        
        for p in players:
            p.draw(win)
            if not p.game_over:
                piece_pos = p.convert_shape_format(p.current_piece)
                top_left_x = p.x_offset
                top_left_y = SCREEN_HEIGHT - (GRID_HEIGHT * BLOCK_SIZE) - 50
                for pos in piece_pos:
                    x, y = pos
                    if y > -1:
                        pygame.draw.rect(win, p.current_piece.color, (top_left_x + x*BLOCK_SIZE, top_left_y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            else:
                font = pygame.font.SysFont('arial', 40)
                lost_text = font.render("GAME OVER", 1, (255, 0, 0))
                win.blit(lost_text, (p.x_offset + 20, SCREEN_HEIGHT/2))

        pygame.display.update()

    pygame.display.quit()

if __name__ == "__main__":
    main()