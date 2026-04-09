import pygame
import random


pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BLOCK_SIZE = 25
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128), 
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]


SHAPES = [
    [['.....', '.....', '..OO.', '..OO.', '.....'], ['.....', '.....', '..OO.', '..OO.', '.....']], 
    [['.....', '..I..', '..I..', '..I..', '..I..'], ['.....', 'IIII.', '.....', '.....', '.....']], 
    [['.....', '.....', '..SS.', '.SS..', '.....'], ['.....', '..S..', '..SS.', '...S.', '.....']], 
    [['.....', '.....', '.ZZ..', '..ZZ.', '.....'], ['.....', '...Z.', '..ZZ.', '..Z..', '.....']], 
    [['.....', '.L...', '.L...', '.LL..', '.....'], ['.....', '...L.', 'LLL..', '.....', '.....'], ['.....', '.LL..', '..L..', '..L..', '.....'], ['.....', '.....', '..LLL', '.L...', '.....']], 
    [['.....', '...J.', '...J.', '..JJ.', '.....'], ['.....', 'JJJ..', '..J..', '.....', '.....'], ['.....', '.JJ..', '.J...', '.J...', '.....'], ['.....', 'J....', 'JJJ..', '.....', '.....']], 
    [['.....', '..T..', '.TTT.', '.....', '.....'], ['.....', '..T..', '..TT.', '..T..', '.....'], ['.....', '.....', '.TTT.', '..T..', '.....'], ['.....', '..T..', '.TT..', '..T..', '.....']]  
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

class PlayerGame:
    def __init__(self, x_offset, controls):
        self.grid = [[BLACK for _ in range(10)] for _ in range(20)]
        self.x_offset = x_offset
        self.controls = controls 
        self.locked_positions = {}
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.27

    def get_shape(self):
        return Piece(5, 0, random.choice(SHAPES))

    def convert_shape_format(self):
        positions = []
        format = self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column != '.':
                    positions.append((self.current_piece.x + j - 2, self.current_piece.y + i - 4))
        return positions

    def valid_space(self):
        accepted_pos = [[(j, i) for j in range(10) if self.grid[i][j] == BLACK] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format()
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self):
        for pos in self.locked_positions:
            x, y = pos
            if y < 1:
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

    def update(self, dt):
        if self.game_over:
            return
            
        self.fall_time += dt
        if self.fall_time/1000 > self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not self.valid_space() and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.lock_piece()

    def lock_piece(self):
        for pos in self.convert_shape_format():
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.get_shape()
        cleared = self.clear_rows()
        self.score += cleared * 10
        if self.check_lost():
            self.game_over = True

    def handle_input(self, event):
        if self.game_over:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls[0]: 
                self.current_piece.x -= 1
                if not self.valid_space():
                    self.current_piece.x += 1
            elif event.key == self.controls[1]: 
                self.current_piece.x += 1
                if not self.valid_space():
                    self.current_piece.x -= 1
            elif event.key == self.controls[2]: 
                self.current_piece.y += 1
                if not self.valid_space():
                    self.current_piece.y -= 1
            elif event.key == self.controls[3]: 
                self.current_piece.rotation += 1
                if not self.valid_space():
                    self.current_piece.rotation -= 1

    def draw(self, surface):
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.locked_positions:
                    self.grid[i][j] = self.locked_positions[(j, i)]
                else:
                    self.grid[i][j] = BLACK

        
        curr_pos = self.convert_shape_format()
        for pos in curr_pos:
            x, y = pos
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, 
                                 (self.x_offset + x*BLOCK_SIZE, y*BLOCK_SIZE + 100, BLOCK_SIZE, BLOCK_SIZE), 0)

        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(surface, GRAY, (self.x_offset + j*BLOCK_SIZE, i*BLOCK_SIZE + 100, BLOCK_SIZE, BLOCK_SIZE), 1)

        
        pygame.draw.rect(surface, WHITE, (self.x_offset, 100, 10*BLOCK_SIZE, 20*BLOCK_SIZE), 3)

        
        font = pygame.font.SysFont('Arial', 24)
        label = font.render(f'Score: {self.score}', 1, WHITE)
        surface.blit(label, (self.x_offset, 70))
        
        if self.game_over:
            lost_label = font.render('GAME OVER', 1, (255, 0, 0))
            surface.blit(lost_label, (self.x_offset + 50, 300))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3-Player Tetris")
    clock = pygame.time.Clock()

    
    p1_controls = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
    p2_controls = [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w]
    p3_controls = [pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_i]

    players = [
        PlayerGame(50, p1_controls),
        PlayerGame(375, p2_controls),
        PlayerGame(700, p3_controls)
    ]

    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for player in players:
                player.handle_input(event)

        for player in players:
            player.update(dt)
            player.draw(screen)

        
        font = pygame.font.SysFont('Arial', 32, bold=True)
        t1 = font.render("PLAYER 1", 1, WHITE)
        t2 = font.render("PLAYER 2", 1, WHITE)
        t3 = font.render("PLAYER 3", 1, WHITE)
        screen.blit(t1, (100, 20))
        screen.blit(t2, (425, 20))
        screen.blit(t3, (750, 20))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()