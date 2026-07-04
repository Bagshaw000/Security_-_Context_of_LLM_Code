import pygame
import random


pygame.font.init()


S_WIDTH = 1200
S_HEIGHT = 750
PLAY_WIDTH = 300  
PLAY_HEIGHT = 600 
BLOCK_SIZE = 30


TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT - 50
P1_X = 50
P2_X = 450
P3_X = 850


SHAPES = [
    [[[1, 1, 1, 1]], [[1], [1], [1], [1]]], 
    [[[1, 1], [1, 1]]], 
    [[[0, 1, 0], [1, 1, 1]], [[1, 0], [1, 1], [1, 0]], [[1, 1, 1], [0, 1, 0]], [[0, 1], [1, 1], [0, 1]]], 
    [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]], 
    [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]], 
    [[[1, 0, 0], [1, 1, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 1, 1], [0, 0, 1]], [[0, 1], [0, 1], [1, 1]]], 
    [[[0, 0, 1], [1, 1, 1]], [[1, 0], [1, 0], [1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1], [0, 1], [0, 1]]]  
]

SHAPE_COLORS = [(0, 255, 255), (255, 255, 0), (128, 0, 128), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)]

class Piece:
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.color = SHAPE_COLORS[shape_idx]
        self.rotation = 0

    def get_current_shape(self):
        return SHAPES[self.shape_idx][self.rotation % len(SHAPES[self.shape_idx])]

def create_grid(locked_pos):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for y in range(20):
        for x in range(10):
            if (x, y) in locked_pos:
                grid[y][x] = locked_pos[(x, y)]
    return grid

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [item for sublist in accepted_pos for item in sublist]
    formatted = piece.get_current_shape()

    for r, row in enumerate(formatted):
        for c, val in enumerate(row):
            if val:
                pos = (piece.x + c, piece.y + r)
                if pos not in accepted_pos:
                    if piece.y + r >= 0:
                        return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.randint(0, len(SHAPES) - 1))

def draw_text_middle(surface, text, size, color, x_offset):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x_offset + PLAY_WIDTH/2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface, x_offset):
    for i in range(20):
        pygame.draw.line(surface, (128, 128, 128), (x_offset, TOP_LEFT_Y + i * BLOCK_SIZE), (x_offset + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
        for j in range(11):
            pygame.draw.line(surface, (128, 128, 128), (x_offset + j * BLOCK_SIZE, TOP_LEFT_Y), (x_offset + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
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

def draw_window(surface, grids, p1_lost, p2_lost, p3_lost):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('3-Player Tetris', 1, (255, 255, 255))
    surface.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), 10))

    offsets = [P1_X, P2_X, P3_X]
    for idx, grid in enumerate(grids):
        x_off = offsets[idx]
        for i in range(20):
            for j in range(10):
                pygame.draw.rect(surface, grid[i][j], (x_off + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        
        pygame.draw.rect(surface, (255, 0, 0), (x_off, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)
        draw_grid(surface, x_off)

    if p1_lost: draw_text_middle(surface, "LOST", 40, (255, 255, 255), P1_X)
    if p2_lost: draw_text_middle(surface, "LOST", 40, (255, 255, 255), P2_X)
    if p3_lost: draw_text_middle(surface, "LOST", 40, (255, 255, 255), P3_X)

    pygame.display.update()

def main():
    locked_p1, locked_p2, locked_p3 = {}, {}, {}
    curr_p1, curr_p2, curr_p3 = get_shape(), get_shape(), get_shape()
    lost_p1, lost_p2, lost_p3 = False, False, False
    
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    run = True
    win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption('3-Player Tetris')

    while run:
        grid1 = create_grid(locked_p1)
        grid2 = create_grid(locked_p2)
        grid3 = create_grid(locked_p3)
        
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            
            if not lost_p1:
                curr_p1.y += 1
                if not valid_space(curr_p1, grid1) and curr_p1.y > 0:
                    curr_p1.y -= 1
                    for r, row in enumerate(curr_p1.get_current_shape()):
                        for c, val in enumerate(row):
                            if val: locked_p1[(curr_p1.x + c, curr_p1.y + r)] = curr_p1.color
                    curr_p1 = get_shape()
                    if check_lost(locked_p1): lost_p1 = True
            
            if not lost_p2:
                curr_p2.y += 1
                if not valid_space(curr_p2, grid2) and curr_p2.y > 0:
                    curr_p2.y -= 1
                    for r, row in enumerate(curr_p2.get_current_shape()):
                        for c, val in enumerate(row):
                            if val: locked_p2[(curr_p2.x + c, curr_p2.y + r)] = curr_p2.color
                    curr_p2 = get_shape()
                    if check_lost(locked_p2): lost_p2 = True
            
            if not lost_p3:
                curr_p3.y += 1
                if not valid_space(curr_p3, grid3) and curr_p3.y > 0:
                    curr_p3.y -= 1
                    for r, row in enumerate(curr_p3.get_current_shape()):
                        for c, val in enumerate(row):
                            if val: locked_p3[(curr_p3.x + c, curr_p3.y + r)] = curr_p3.color
                    curr_p3 = get_shape()
                    if check_lost(locked_p3): lost_p3 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                
                if not lost_p1:
                    if event.key == pygame.K_LEFT:
                        curr_p1.x -= 1
                        if not valid_space(curr_p1, grid1): curr_p1.x += 1
                    if event.key == pygame.K_RIGHT:
                        curr_p1.x += 1
                        if not valid_space(curr_p1, grid1): curr_p1.x -= 1
                    if event.key == pygame.K_DOWN:
                        curr_p1.y += 1
                        if not valid_space(curr_p1, grid1): curr_p1.y -= 1
                    if event.key == pygame.K_UP:
                        curr_p1.rotation += 1
                        if not valid_space(curr_p1, grid1): curr_p1.rotation -= 1
                
                if not lost_p2:
                    if event.key == pygame.K_a:
                        curr_p2.x -= 1
                        if not valid_space(curr_p2, grid2): curr_p2.x += 1
                    if event.key == pygame.K_d:
                        curr_p2.x += 1
                        if not valid_space(curr_p2, grid2): curr_p2.x -= 1
                    if event.key == pygame.K_s:
                        curr_p2.y += 1
                        if not valid_space(curr_p2, grid2): curr_p2.y -= 1
                    if event.key == pygame.K_w:
                        curr_p2.rotation += 1
                        if not valid_space(curr_p2, grid2): curr_p2.rotation -= 1
                
                if not lost_p3:
                    if event.key == pygame.K_j:
                        curr_p3.x -= 1
                        if not valid_space(curr_p3, grid3): curr_p3.x += 1
                    if event.key == pygame.K_l:
                        curr_p3.x += 1
                        if not valid_space(curr_p3, grid3): curr_p3.x -= 1
                    if event.key == pygame.K_k:
                        curr_p3.y += 1
                        if not valid_space(curr_p3, grid3): curr_p3.y -= 1
                    if event.key == pygame.K_i:
                        curr_p3.rotation += 1
                        if not valid_space(curr_p3, grid3): curr_p3.rotation -= 1

        
        p1_shape = curr_p1.get_current_shape()
        for r, row in enumerate(p1_shape):
            for c, val in enumerate(row):
                if val and curr_p1.y + r >= 0:
                    grid1[curr_p1.y + r][curr_p1.x + c] = curr_p1.color
        
        p2_shape = curr_p2.get_current_shape()
        for r, row in enumerate(p2_shape):
            for c, val in enumerate(row):
                if val and curr_p2.y + r >= 0:
                    grid2[curr_p2.y + r][curr_p2.x + c] = curr_p2.color

        p3_shape = curr_p3.get_current_shape()
        for r, row in enumerate(p3_shape):
            for c, val in enumerate(row):
                if val and curr_p3.y + r >= 0:
                    grid3[curr_p3.y + r][curr_p3.x + c] = curr_p3.color

        clear_rows(grid1, locked_p1)
        clear_rows(grid2, locked_p2)
        clear_rows(grid3, locked_p3)

        draw_window(win, [grid1, grid2, grid3], lost_p1, lost_p2, lost_p3)
        
        if lost_p1 and lost_p2 and lost_p3:
            run = False

    pygame.display.quit()

if __name__ == "__main__":
    main()