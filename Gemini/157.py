import pygame
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
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
    [['.....', '.O...', '.OOO.', '.....', '.....'], ['.....', '..OO.', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '...O.', '.....'], ['.....', '..O..', '..O..', '.OO..', '.....']], 
    [['.....', '...O.', '.OOO.', '.....', '.....'], ['.....', '..O..', '..O..', '..OO.', '.....'], ['.....', '.....', '.OOO.', '.O...', '.....'], ['.....', '.OO..', '..O..', '..O..', '.....']], 
    [['.....', '..O..', '.OOO.', '.....', '.....'], ['.....', '..O..', '..OO.', '..O..', '.....'], ['.....', '.....', '.OOO.', '..O..', '.....'], ['.....', '..O..', '.OO..', '..O..', '.....']]  
]

class Piece:
    
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.color = COLORS[shape_idx]
        self.rotation = 0
        self.shape = SHAPES[shape_idx]

class TetrisEngine:
    
    def __init__(self, x_offset, player_name):
        self.x_offset = x_offset
        self.player_name = player_name
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.game_over = False
        self.score = 0
        self.locked_pos = {} 

    def get_new_piece(self):
        return Piece(5, 0, random.randint(0, len(SHAPES) - 1))

    def convert_shape_format(self, piece):
        positions = []
        format = piece.shape[piece.rotation % len(piece.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == 'O':
                    positions.append((piece.x + j - 2, piece.y + i - 4))
        return positions

    def valid_space(self, piece):
        accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if self.grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
        accepted_pos = [item for sublist in accepted_pos for item in sublist]

        formatted = self.convert_shape_format(piece)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_game_over(self):
        for pos in self.locked_pos:
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
                        del self.locked_pos[(j, i)]
                    except:
                        continue
        
        if inc > 0:
            for key in sorted(list(self.locked_pos.keys()), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.locked_pos[newKey] = self.locked_pos.pop(key)
        
        self.score += (inc * 100)

    def update_grid(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.locked_pos:
                    self.grid[i][j] = self.locked_pos[(j, i)]

    def drop_piece(self):
        if not self.game_over:
            self.current_piece.y += 1
            if not self.valid_space(self.current_piece):
                self.current_piece.y -= 1
                self.lock_piece()

    def lock_piece(self):
        for pos in self.convert_shape_format(self.current_piece):
            self.locked_pos[pos] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        self.clear_rows()
        if self.check_game_over():
            self.game_over = True

    def move_left(self):
        self.current_piece.x -= 1
        if not self.valid_space(self.current_piece):
            self.current_piece.x += 1

    def move_right(self):
        self.current_piece.x += 1
        if not self.valid_space(self.current_piece):
            self.current_piece.x -= 1

    def rotate(self):
        self.current_piece.rotation += 1
        if not self.valid_space(self.current_piece):
            self.current_piece.rotation -= 1

class ThreePlayerTetris:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Amazon Engineering Design - 3 Player Tetris")
        self.clock = pygame.time.Clock()
        
        
        
        self.players = [
            TetrisEngine(50, "Player 1"),
            TetrisEngine(450, "Player 2"),
            TetrisEngine(850, "Player 3")
        ]
        self.fall_time = 0
        self.fall_speed = 0.27

    def draw_window(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont('arial', 30)
        label = font.render('3-Player Tetris System', 1, WHITE)
        self.screen.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, 10))

        for player in self.players:
            
            for i in range(GRID_HEIGHT):
                for j in range(GRID_WIDTH):
                    pygame.draw.rect(self.screen, player.grid[i][j], 
                                     (player.x_offset + j * BLOCK_SIZE, 100 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            
            
            piece_pos = player.convert_shape_format(player.current_piece)
            for pos in piece_pos:
                x, y = pos
                if y > -1:
                    pygame.draw.rect(self.screen, player.current_piece.color,
                                     (player.x_offset + x * BLOCK_SIZE, 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

            
            pygame.draw.rect(self.screen, (255, 0, 0), (player.x_offset, 100, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 4)

            
            p_label = font.render(player.player_name, 1, WHITE)
            s_label = font.render(f'Score: {player.score}', 1, WHITE)
            self.screen.blit(p_label, (player.x_offset, 60))
            self.screen.blit(s_label, (player.x_offset, 100 + GRID_HEIGHT * BLOCK_SIZE + 10))
            
            if player.game_over:
                go_label = font.render('GAME OVER', 1, (255, 0, 0))
                self.screen.blit(go_label, (player.x_offset + 30, 100 + (GRID_HEIGHT * BLOCK_SIZE) / 2))

    def run(self):
        run = True
        while run:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            
            if self.fall_time / 1000 >= self.fall_speed:
                self.fall_time = 0
                for player in self.players:
                    player.drop_piece()
                    player.update_grid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    
                    if not self.players[0].game_over:
                        if event.key == pygame.K_a: self.players[0].move_left()
                        if event.key == pygame.K_d: self.players[0].move_right()
                        if event.key == pygame.K_s: self.players[0].drop_piece()
                        if event.key == pygame.K_w: self.players[0].rotate()

                    
                    if not self.players[1].game_over:
                        if event.key == pygame.K_LEFT: self.players[1].move_left()
                        if event.key == pygame.K_RIGHT: self.players[1].move_right()
                        if event.key == pygame.K_DOWN: self.players[1].drop_piece()
                        if event.key == pygame.K_UP: self.players[1].rotate()

                    
                    if not self.players[2].game_over:
                        if event.key == pygame.K_j: self.players[2].move_left()
                        if event.key == pygame.K_l: self.players[2].move_right()
                        if event.key == pygame.K_k: self.players[2].drop_piece()
                        if event.key == pygame.K_i: self.players[2].rotate()

            self.draw_window()
            pygame.display.update()

if __name__ == "__main__":
    game = ThreePlayerTetris()
    game.run()