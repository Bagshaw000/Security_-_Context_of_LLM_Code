import pygame
import random



pygame.init()



SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
BLOCK_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128), 
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 127, 0)
]



SHAPES = [
    [['.....', '.....', '..OO.', '..OO.', '.....']], 
    [['.....', '..O..', '..O..', '..O..', '..O..'], ['.....', 'OOOO.', '.....', '.....', '.....']], 
    [['.....', '..O..', '.OOO.', '.....', '.....'], ['.....', '..O..', '..OO.', '..O..', '.....'], ['.....', '.....', '.OOO.', '..O..', '.....'], ['.....', '..O..', '.OO..', '..O..', '.....']], 
    [['.....', '...O.', '.OOO.', '.....', '.....'], ['.....', '..O..', '..O..', '..OO.', '.....'], ['.....', '.....', '.OOO.', '.O...', '.....'], ['.....', '.OO..', '..O..', '..O..', '.....']], 
    [['.....', '.O...', '.OOO.', '.....', '.....'], ['.....', '..OO.', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '...O.', '.....'], ['.....', '..O..', '..O..', '.OO..', '.....']], 
    [['.....', '..OO.', '.OO..', '.....', '.....'], ['.....', '..O..', '..OO.', '...O.', '.....']], 
    [['.....', '.OO..', '..OO.', '.....', '.....'], ['.....', '...O.', '..OO.', '..O..', '.....']]  
]

class Piece:
    
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

def create_grid(locked_pos={}):
    
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_pos:
                grid[y][x] = locked_pos[(x, y)]
    return grid

def convert_shape_format(piece):
    
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(piece, grid):
    
    accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(piece)
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

def draw_grid(surface, grid, x_offset, y_offset):
    
    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (x_offset, y_offset + i*BLOCK_SIZE), (x_offset + GRID_WIDTH*BLOCK_SIZE, y_offset + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRAY, (x_offset + j*BLOCK_SIZE, y_offset), (x_offset + j*BLOCK_SIZE, y_offset + GRID_HEIGHT*BLOCK_SIZE))

def draw_window(surface, grids, x_offsets, scores):
    
    surface.fill(BLACK)
    font = pygame.font.SysFont('arial', 30)
    label = font.render('3-Player Tetris', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH / 2 - (label.get_width() / 2), 10))

    
    controls_font = pygame.font.SysFont('arial', 18)
    p1_ctrl = controls_font.render('P1: W-A-S-D', 1, WHITE)
    p2_ctrl = controls_font.render('P2: I-J-K-L', 1, WHITE)
    p3_ctrl = controls_font.render('P3: Arrows', 1, WHITE)
    
    surface.blit(p1_ctrl, (x_offsets[0], 60))
    surface.blit(p2_ctrl, (x_offsets[1], 60))
    surface.blit(p3_ctrl, (x_offsets[2], 60))

    for i in range(3):
        
        score_label = font.render(f'Score: {scores[i]}', 1, WHITE)
        surface.blit(score_label, (x_offsets[i], 650))
        
        
        for row in range(len(grids[i])):
            for col in range(len(grids[i][row])):
                pygame.draw.rect(surface, grids[i][row][col], (x_offsets[i] + col*BLOCK_SIZE, 100 + row*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        
        draw_grid(surface, grids[i], x_offsets[i], 100)
        pygame.draw.rect(surface, (255, 0, 0), (x_offsets[i], 100, GRID_WIDTH*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE), 4)

    pygame.display.update()

def main():
    
    
    locked_positions = [{}, {}, {}]
    grids = [create_grid(), create_grid(), create_grid()]
    change_pieces = [False, False, False]
    run = True
    current_pieces = [get_shape(), get_shape(), get_shape()]
    next_pieces = [get_shape(), get_shape(), get_shape()]
    scores = [0, 0, 0]
    lost = [False, False, False]
    
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    x_offsets = [50, 400, 750]

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Three-Player Tetris')

    while run:
        grids = [create_grid(locked_positions[i]) for i in range(3)]
        fall_time += clock.get_rawtime()
        clock.tick()

        
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            for i in range(3):
                if not lost[i]:
                    current_pieces[i].y += 1
                    if not (valid_space(current_pieces[i], grids[i])) and current_pieces[i].y > 0:
                        current_pieces[i].y -= 1
                        change_pieces[i] = True

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                
                if not lost[0]:
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

                
                if not lost[1]:
                    if event.key == pygame.K_j:
                        current_pieces[1].x -= 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].x += 1
                    if event.key == pygame.K_l:
                        current_pieces[1].x += 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].x -= 1
                    if event.key == pygame.K_k:
                        current_pieces[1].y += 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].y -= 1
                    if event.key == pygame.K_i:
                        current_pieces[1].rotation += 1
                        if not valid_space(current_pieces[1], grids[1]): current_pieces[1].rotation -= 1

                
                if not lost[2]:
                    if event.key == pygame.K_LEFT:
                        current_pieces[2].x -= 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].x += 1
                    if event.key == pygame.K_RIGHT:
                        current_pieces[2].x += 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].x -= 1
                    if event.key == pygame.K_DOWN:
                        current_pieces[2].y += 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].y -= 1
                    if event.key == pygame.K_UP:
                        current_pieces[2].rotation += 1
                        if not valid_space(current_pieces[2], grids[2]): current_pieces[2].rotation -= 1

        
        for i in range(3):
            if not lost[i]:
                shape_pos = convert_shape_format(current_pieces[i])
                for pos in shape_pos:
                    x, y = pos
                    if y > -1:
                        grids[i][y][x] = current_pieces[i].color

                
                if change_pieces[i]:
                    for pos in shape_pos:
                        p = (pos[0], pos[1])
                        locked_positions[i][p] = current_pieces[i].color
                    current_pieces[i] = next_pieces[i]
                    next_pieces[i] = get_shape()
                    change_pieces[i] = False
                    scores[i] += clear_rows(grids[i], locked_positions[i]) * 10
                    
                    if check_lost(locked_positions[i]):
                        lost[i] = True

        draw_window(win, grids, x_offsets, scores)
        
        
        if all(lost):
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()