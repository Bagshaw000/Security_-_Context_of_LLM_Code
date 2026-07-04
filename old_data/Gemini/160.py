import pygame
import random








pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BLOCK_SIZE = 25  
FPS = 60 


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255), (0, 0, 255), (255, 165, 0),
    (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)
]



SHAPES = [
    [['.....', '.....', '..OO.', '..OO.', '.....'], ['.....', '.....', '..OO.', '..OO.', '.....']], 
    [['.....', '..O..', '..O..', '..O..', '..O..'], ['.....', '.....', 'OOOO.', '.....', '.....']], 
    [['.....', '..O..', '.OOO.', '.....', '.....'], ['.....', '..O..', '..OO.', '..O..', '.....'], ['.....', '.....', '.OOO.', '..O..', '.....'], ['.....', '..O..', '.OO..', '..O..', '.....']], 
    [['.....', '...O.', '.OOO.', '.....', '.....'], ['.....', '..O..', '..O..', '..OO.', '.....'], ['.....', '.....', '.OOO.', '.O...', '.....'], ['.....', '.OO..', '..O..', '..O..', '.....']], 
    [['.....', '.O...', '.OOO.', '.....', '.....'], ['.....', '..OO.', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '...O.', '.....'], ['.....', '..O..', '..O..', '.OO..', '.....']], 
    [['.....', '..OO.', '.OO..', '.....', '.....'], ['.....', '..O..', '..OO.', '...O.', '.....']], 
    [['.....', '.OO..', '..OO.', '.....', '.....'], ['.....', '...O.', '..OO.', '..O..', '.....']]  
]



class PlayerBoard:
    def __init__(self, x_offset, controls):
        self.width = 10 
        self.height = 20 
        self.x_offset = x_offset 
        self.controls = controls 
        self.grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.5 

    def get_new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': self.width // 2 - 2,
            'y': -2,
            'rotation': 0
        }

    def convert_shape_format(self, piece):
        positions = []
        format = piece['shape'][piece['rotation'] % len(piece['shape'])]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == 'O':
                    positions.append((piece['x'] + j, piece['y'] + i))
        return positions

    def valid_space(self, piece):
        accepted_pos = [[(j, i) for j in range(self.width) if self.grid[i][j] == BLACK] for i in range(self.height)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format(piece)
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def clear_lines(self):
        lines_to_clear = 0
        for i in range(len(self.grid) - 1, -1, -1):
            row = self.grid[i]
            if BLACK not in row:
                lines_to_clear += 1
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(self.width)])
        self.score += lines_to_clear * 100

    def update(self, dt):
        if self.game_over: return
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            self.current_piece['y'] += 1
            if not self.valid_space(self.current_piece):
                self.current_piece['y'] -= 1
                self.lock_piece()

    def lock_piece(self):
        for pos in self.convert_shape_format(self.current_piece):
            p_x, p_y = pos
            if p_y >= 0:
                self.grid[p_y][p_x] = self.current_piece['color']
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        self.clear_lines()
        if not self.valid_space(self.current_piece):
            self.game_over = True

    def move(self, dx, dy):
        if self.game_over: return
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy
        if not self.valid_space(self.current_piece):
            self.current_piece['x'] -= dx
            self.current_piece['y'] -= dy
            return False
        return True

    def rotate(self):
        if self.game_over: return
        self.current_piece['rotation'] += 1
        if not self.valid_space(self.current_piece):
            self.current_piece['rotation'] -= 1

    def draw(self, surface):
        
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(surface, self.grid[i][j], (self.x_offset + j*BLOCK_SIZE, 50 + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        
        if not self.game_over:
            formatted = self.convert_shape_format(self.current_piece)
            for pos in formatted:
                x, y = pos
                if y >= 0:
                    pygame.draw.rect(surface, self.current_piece['color'], (self.x_offset + x*BLOCK_SIZE, 50 + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        
        pygame.draw.rect(surface, WHITE, (self.x_offset, 50, self.width*BLOCK_SIZE, self.height*BLOCK_SIZE), 2)
        
        
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (self.x_offset, 10))
        if self.game_over:
            over_text = font.render("GAME OVER", True, (255, 0, 0))
            surface.blit(over_text, (self.x_offset, 50 + (self.height*BLOCK_SIZE)//2))


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Three Player Tetris")
    clock = pygame.time.Clock()

    
    
    
    
    p1_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP}
    p2_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w}
    p3_controls = {'left': pygame.K_j, 'right': pygame.K_l, 'down': pygame.K_k, 'rotate': pygame.K_i}

    players = [
        PlayerBoard(100, p1_controls),
        PlayerBoard(475, p2_controls),
        PlayerBoard(850, p3_controls)
    ]

    running = True
    while running:
        dt = clock.get_rawtime() / 1000.0
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                for p in players:
                    if event.key == p.controls['left']:
                        p.move(-1, 0)
                    if event.key == p.controls['right']:
                        p.move(1, 0)
                    if event.key == p.controls['down']:
                        p.move(0, 1)
                    if event.key == p.controls['rotate']:
                        p.rotate()

        screen.fill(BLACK)
        
        
        font = pygame.font.SysFont('Arial', 18)
        instr1 = font.render("P1: Arrows", True, WHITE)
        instr2 = font.render("P2: WASD", True, WHITE)
        instr3 = font.render("P3: IJKL", True, WHITE)
        screen.blit(instr1, (100, SCREEN_HEIGHT - 40))
        screen.blit(instr2, (475, SCREEN_HEIGHT - 40))
        screen.blit(instr3, (850, SCREEN_HEIGHT - 40))

        for p in players:
            p.update(dt)
            p.draw(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()