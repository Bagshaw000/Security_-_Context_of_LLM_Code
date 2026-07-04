import pygame
import random


BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
SHAPES_COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]


SHAPES = [
    [['.....', '.....', 'OOOO.', '.....', '.....'],
     ['..O..', '..O..', '..O..', '..O..', '.....']],  
    [['.....', '.....', '.OO..', '.OO..', '.....']],  
    [['.....', '..O..', '.OOO.', '.....', '.....'],
     ['.....', '..O..', '..OO.', '..O..', '.....'],
     ['.....', '.....', '.OOO.', '..O..', '.....'],
     ['.....', '..O..', '.OO..', '..O..', '.....']],  
    [['.....', '.....', '..OO.', '.OO..', '.....'],
     ['.....', '.O...', '.OO..', '..O..', '.....']],  
    [['.....', '.....', '.OO..', '..OO.', '.....'],
     ['.....', '..O..', '.OO..', '.O...', '.....']],  
    [['.....', '.O...', '.OOO.', '.....', '.....'],
     ['.....', '..OO.', '..O..', '..O..', '.....'],
     ['.....', '.....', '.OOO.', '...O.', '.....'],
     ['.....', '..O..', '..O..', '.OO..', '.....']],  
    [['.....', '...O.', '.OOO.', '.....', '.....'],
     ['.....', '..O..', '..O..', '..OO.', '.....'],
     ['.....', '.....', '.OOO.', '.O...', '.....'],
     ['.....', '.OO..', '..O..', '..O..', '.....']]   
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(SHAPES_COLORS)
        self.rotation = 0

class TetrisPlayer:
    def __init__(self, x_offset, name, controls):
        self.x_offset = x_offset
        self.name = name
        self.controls = controls 
        self.grid = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.5 

    def get_new_piece(self):
        return Piece(5, 0, random.choice(SHAPES))

    def convert_shape_format(self):
        positions = []
        format = self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == 'O':
                    positions.append((self.current_piece.x + j, self.current_piece.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions

    def valid_space(self):
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == (0, 0, 0)] for i in range(GRID_HEIGHT)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format()
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self):
        for pos in self.convert_shape_format():
            if pos[1] < 0:
                return True
        return False

    def clear_lines(self):
        inc = 0
        for i in range(len(self.grid) - 1, -1, -1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.grid[i][j]
                    except:
                        continue
        if inc > 0:
            for _ in range(inc):
                self.grid.insert(0, [(0, 0, 0) for _ in range(GRID_WIDTH)])
                self.grid.pop(len(self.grid) - 1)
            self.score += inc * 10

    def update(self, dt):
        if self.game_over:
            return

        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not self.valid_space() and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.lock_piece()

    def lock_piece(self):
        for pos in self.convert_shape_format():
            p = (pos[0], pos[1])
            self.grid[p[1]][p[0]] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        self.clear_lines()
        if self.check_lost():
            self.game_over = True

    def handle_input(self, event):
        if self.game_over:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls['left']:
                self.current_piece.x -= 1
                if not self.valid_space():
                    self.current_piece.x += 1
            elif event.key == self.controls['right']:
                self.current_piece.x += 1
                if not self.valid_space():
                    self.current_piece.x -= 1
            elif event.key == self.controls['down']:
                self.current_piece.y += 1
                if not self.valid_space():
                    self.current_piece.y -= 1
            elif event.key == self.controls['rotate']:
                self.current_piece.rotation += 1
                if not self.valid_space():
                    self.current_piece.rotation -= 1

    def draw(self, surface):
        
        start_x = self.x_offset
        start_y = 100
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(surface, self.grid[i][j], 
                                 (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        
        formatted = self.convert_shape_format()
        for pos in formatted:
            x, y = pos
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, 
                                 (start_x + x * BLOCK_SIZE, start_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        
        pygame.draw.rect(surface, (255, 0, 0), (start_x, start_y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 4)
        
        
        font = pygame.font.SysFont('Arial', 30)
        label = font.render(f"{self.name}: {self.score}", 1, WHITE)
        surface.blit(label, (start_x, start_y - 40))
        
        if self.game_over:
            lost_label = font.render("GAME OVER", 1, (255, 0, 0))
            surface.blit(lost_label, (start_x + 20, start_y + 200))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3 Player Tetris")
    clock = pygame.time.Clock()

    
    
    p1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w}
    
    p2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP}
    
    p3_controls = {'left': pygame.K_j, 'right': pygame.K_l, 'down': pygame.K_k, 'rotate': pygame.K_i}

    players = [
        TetrisPlayer(50, "P1 (WASD)", p1_controls),
        TetrisPlayer(375, "P2 (Arrows)", p2_controls),
        TetrisPlayer(700, "P3 (IJKL)", p3_controls)
    ]

    running = True
    while running:
        dt = clock.get_rawtime() / 1000.0
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for player in players:
                player.handle_input(event)

        screen.fill(BLACK)

        
        for player in players:
            player.update(dt)
            player.draw(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()