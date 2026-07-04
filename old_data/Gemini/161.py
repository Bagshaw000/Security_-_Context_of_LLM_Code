import pygame
import random





pygame.font.init()


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  
PLAY_HEIGHT = 600 
BLOCK_SIZE = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


S = [['.....', '.....', '..00.', '.00..', '.....'],
     ['.....', '..0..', '..00.', '...0.', '.....']]

Z = [['.....', '.....', '.00..', '..00.', '.....'],
     ['.....', '..0..', '.00..', '.0..', '.....']]

I = [['..0..', '..0..', '..0..', '..0..', '.....'],
     ['.....', '0000.', '.....', '.....', '.....']]

O = [['.....', '.....', '.00..', '.00..', '.....']]

J = [['.....', '.0...', '.000.', '.....', '.....'],
     ['.....', '..00.', '..0..', '..0..', '.....'],
     ['.....', '.....', '.000.', '...0.', '.....'],
     ['.....', '..0..', '..0..', '.00..', '.....']]

L = [['.....', '...0.', '.000.', '.....', '.....'],
     ['.....', '..0..', '..0..', '..00.', '.....'],
     ['.....', '.....', '.000.', '.0...', '.....'],
     ['.....', '.00..', '..0..', '..0..', '.....']]

T = [['.....', '..0..', '.000.', '.....', '.....'],
     ['.....', '..0..', '..00.', '..0..', '.....'],
     ['.....', '.....', '.000.', '..0..', '.....'],
     ['.....', '..0..', '.00..', '..0..', '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_grid(surface, x_offset):
    for i in range(20):
        pygame.draw.line(surface, GRAY, (x_offset, i*BLOCK_SIZE), (x_offset + PLAY_WIDTH, i*BLOCK_SIZE))
        for j in range(11):
            pygame.draw.line(surface, GRAY, (x_offset + j*BLOCK_SIZE, 0), (x_offset + j*BLOCK_SIZE, PLAY_HEIGHT))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked.keys()), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_window(surface, grids, x_offsets, scores):
    surface.fill(BLACK)
    font = pygame.font.SysFont('arial', 30)
    label = font.render('3-Player Tetris', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, 10))

    for idx, grid in enumerate(grids):
        x_off = x_offsets[idx]
        
        s_label = font.render(f'P{idx+1} Score: {scores[idx]}', 1, WHITE)
        surface.blit(s_label, (x_off, PLAY_HEIGHT + 20))
        
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (x_off + j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        
        pygame.draw.rect(surface, (255, 0, 0), (x_off, 0, PLAY_WIDTH, PLAY_HEIGHT), 2)
        draw_grid(surface, x_off)

def main():
    
    x_offsets = [50, 400, 750]
    locked_positions = [{}, {}, {}]
    grids = [create_grid(), create_grid(), create_grid()]
    
    change_piece = [False, False, False]
    run = True
    current_pieces = [get_shape(), get_shape(), get_shape()]
    next_pieces = [get_shape(), get_shape(), get_shape()]
    clock = pygame.time.Clock()
    fall_time = [0, 0, 0]
    fall_speed = 0.27
    scores = [0, 0, 0]
    game_over = [False, False, False]

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('3-Player Tetris')

    while run:
        grids = [create_grid(locked_positions[i]) for i in range(3)]
        dt = clock.tick()
        for i in range(3):
            if not game_over[i]:
                fall_time[i] += dt
                if fall_time[i] / 1000 >= fall_speed:
                    fall_time[i] = 0
                    current_pieces[i].y += 1
                    if not (valid_space(current_pieces[i], grids[i])) and current_pieces[i].y > 0:
                        current_pieces[i].y -= 1
                        change_piece[i] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                
                if not game_over[0]:
                    if event.key == pygame.K_a:
                        current_pieces[0].x -= 1
                        if not valid_space(current_pieces[0], grids[0]): current_pieces[0].x += 1
                    if event.key == pygame.K_d:
                        current_pieces[0].x += 1
                        if not valid_space(current_pieces[0], grids[0]): current_pieces[0].x -= 1
                    if event.key == pygame.K_s:
                        current_pieces[0].y += 1
                        if not valid_space(current_pieces[0], grids[0]): current_pieces[0].y -= 1
                    if event.key == pygame.K_w:
                        current_pieces[0].rotation += 1
                        if not valid_space(current_pieces[0], grids[0]): current_pieces[0].rotation -= 1

                
                if not game_over[1]:
                    if event.key == pygame.K_LEFT:
                        current_pieces[1].x -= 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].x += 1
                    if event.key == pygame.K_RIGHT:
                        current_pieces[1].x += 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].x -= 1
                    if event.key == pygame.K_DOWN:
                        current_pieces[1].y += 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].y -= 1
                    if event.key == pygame.K_UP:
                        current_pieces[1].rotation += 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].rotation -= 1

                
                if not game_over[2]:
                    if event.key == pygame.K_j:
                        current_pieces[2].x -= 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].x += 1
                    if event.key == pygame.K_l:
                        current_pieces[2].x += 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].x -= 1
                    if event.key == pygame.K_k:
                        current_pieces[2].y += 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].y -= 1
                    if event.key == pygame.K_i:
                        current_pieces[2].rotation += 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].rotation -= 1

        for i in range(3):
            if game_over[i]: continue
            
            shape_pos = convert_shape_format(current_pieces[i])
            for pos in shape_pos:
                if pos[1] > -1:
                    grids[i][pos[1]][pos[0]] = current_pieces[i].color

            if change_piece[i]:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[i][p] = current_pieces[i].color
                current_pieces[i] = next_pieces[i]
                next_pieces[i] = get_shape()
                change_piece[i] = False
                scores[i] += clear_rows(grids[i], locked_positions[i]) * 10

                if check_lost(locked_positions[i]):
                    game_over[i] = True

        draw_window(win, grids, x_offsets, scores)
        pygame.display.update()

        if all(game_over):
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()