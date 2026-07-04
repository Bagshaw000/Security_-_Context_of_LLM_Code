import pygame
import random













pygame.font.init()


S_WIDTH = 1100
S_HEIGHT = 750
PLAY_WIDTH = 300  
PLAY_HEIGHT = 600 
BLOCK_SIZE = 30


S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
I = [['..0..', '..0..', '..0..', '..0..', '.....'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.010.', '..0..', '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
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
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
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

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked.keys()), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_window(surface, grids, scores, game_overs):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('3-Player Tetris', 1, (255, 255, 255))
    surface.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), 10))

    offsets = [50, 400, 750]
    player_names = ["Harold P1", "Harold P2", "Harold P3"]

    for i in range(3):
        
        s_font = pygame.font.SysFont('comicsans', 30)
        score_label = s_font.render('Score: ' + str(scores[i]), 1, (255,255,255))
        surface.blit(score_label, (offsets[i], 670))
        
        name_label = s_font.render(player_names[i], 1, (255,255,255))
        surface.blit(name_label, (offsets[i], 30))

        
        for r in range(len(grids[i])):
            for c in range(len(grids[i][r])):
                pygame.draw.rect(surface, grids[i][r][c], (offsets[i] + c*BLOCK_SIZE, 70 + r*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        
        pygame.draw.rect(surface, (255, 255, 255), (offsets[i], 70, PLAY_WIDTH, PLAY_HEIGHT), 4)

        if game_overs[i]:
            go_label = font.render('GAME OVER', 1, (255,0,0))
            surface.blit(go_label, (offsets[i] + 30, 300))

    pygame.display.update()

def main():
    locked_positions = [{}, {}, {}]
    grids = [create_grid(), create_grid(), create_grid()]
    change_piece = [False, False, False]
    run = True
    current_pieces = [get_shape(), get_shape(), get_shape()]
    next_pieces = [get_shape(), get_shape(), get_shape()]
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    scores = [0, 0, 0]
    game_overs = [False, False, False]

    win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption('Triple Tetris')

    while run:
        grids = [create_grid(locked_positions[i]) for i in range(3)]
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            for i in range(3):
                if not game_overs[i]:
                    current_pieces[i].y += 1
                    if not (valid_space(current_pieces[i], grids[i])) and current_pieces[i].y > 0:
                        current_pieces[i].y -= 1
                        change_piece[i] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                
                if not game_overs[0]:
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

                
                if not game_overs[1]:
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

                
                if not game_overs[2]:
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
            if not game_overs[i]:
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
                        game_overs[i] = True

        draw_window(win, grids, scores, game_overs)
        
        if all(game_overs):
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()