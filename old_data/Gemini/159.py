import pygame
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  
    (255, 255, 0),  
    (128, 0, 128),  
    (0, 255, 0),    
    (255, 0, 0),    
    (0, 0, 255),    
    (255, 165, 0)   
]


SHAPES = [
    [['.....', '.....', '..OO.', '..OO.', '.....'], ['.....', '.....', '..OO.', '..OO.', '.....']], 
    [['.....', '..O..', '..O..', '..O..', '..O..'], ['.....', 'OOOO.', '.....', '.....', '.....']], 
    [['.....', '.....', '..OO.', '.OO..', '.....'], ['.....', '.O...', '.OO..', '..O..', '.....']], 
    [['.....', '.....', '.OO..', '..OO.', '.....'], ['.....', '..O..', '.OO..', '.O...', '.....']], 
    [['.....', '..O..', '..O..', '..OO.', '.....'], ['.....', '...O.', '.OOO.', '.....', '.....'], ['.....', '.OO..', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '.O...', '.....']], 
    [['.....', '..O..', '..O..', '.OO..', '.....'], ['.....', '.O...', '.OOO.', '.....', '.....'], ['.....', '..OO.', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '...O.', '.....']], 
    [['.....', '..O..', '.OOO.', '.....', '.....'], ['.....', '..O..', '..OO.', '..O..', '.....'], ['.....', '.....', '.OOO.', '..O..', '.....'], ['.....', '..O..', '.OO..', '..O..', '.....']]  
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

class TetrisGame:
    def __init__(self, x_offset, player_name, controls):
        self.x_offset = x_offset
        self.player_name = player_name
        self.controls = controls 
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.locked_positions = {} 
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.27

    def get_shape(self):
        return Piece(5, 0, random.choice(SHAPES))

    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == 'O':
                    positions.append((shape.x + j - 2, shape.y + i - 4))
        return positions

    def valid_space(self, shape):
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format(shape)
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
        if self.fall_time/1000 >= self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not self.valid_space(self.current_piece) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.lock_piece()

    def lock_piece(self):
        for pos in self.convert_shape_format(self.current_piece):
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.get_shape()
        rows_cleared = self.clear_rows()
        self.score += rows_cleared * 10
        if self.check_lost():
            self.game_over = True

    def handle_input(self, event):
        if self.game_over:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls['left']:
                self.current_piece.x -= 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.x += 1
            elif event.key == self.controls['right']:
                self.current_piece.x += 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.x -= 1
            elif event.key == self.controls['down']:
                self.current_piece.y += 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.y -= 1
            elif event.key == self.controls['rotate']:
                self.current_piece.rotation += 1
                if not self.valid_space(self.current_piece):
                    self.current_piece.rotation -= 1

    def draw(self, surface):
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                self.grid[i][j] = self.locked_positions.get((j, i), BLACK)

        
        formatted = self.convert_shape_format(self.current_piece)
        for i in range(len(formatted)):
            x, y = formatted[i]
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, 
                                (self.x_offset + x*BLOCK_SIZE, y*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE), 0)

        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(surface, self.grid[i][j], 
                                (self.x_offset + j*BLOCK_SIZE, i*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(surface, GRAY, 
                                (self.x_offset + j*BLOCK_SIZE, i*BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE), 1)

        
        pygame.draw.rect(surface, WHITE, (self.x_offset, 50, GRID_WIDTH*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE), 4)
        
        
        font = pygame.font.SysFont('arial', 20)
        label = font.render(f"{self.player_name}: {self.score}", 1, WHITE)
        surface.blit(label, (self.x_offset, 20))
        if self.game_over:
            lost_label = font.render("GAME OVER", 1, (255, 0, 0))
            surface.blit(lost_label, (self.x_offset + 50, 300))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Three Player Tetris - Principal Edition")
    clock = pygame.time.Clock()

    
    p1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w}
    p2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP}
    p3_controls = {'left': pygame.K_j, 'right': pygame.K_l, 'down': pygame.K_k, 'rotate': pygame.K_i}

    
    players = [
        TetrisGame(100, "Player 1 (WASD)", p1_controls),
        TetrisGame(475, "Player 2 (Arrows)", p2_controls),
        TetrisGame(850, "Player 3 (IJKL)", p3_controls)
    ]

    running = True
    while running:
        dt = clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for player in players:
                player.handle_input(event)

        for player in players:
            player.update(dt)
            player.draw(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()