import pygame
import random







pygame.font.init()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20


S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
I = [['..0..', '..0..', '..0..', '..0..', '.....'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_pos):
    grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
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
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == (0,0,0)] for i in range(GRID_HEIGHT)]
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
        if (0,0,0) not in row:
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
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (x_offset + j*BLOCK_SIZE, y_offset + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    pygame.draw.rect(surface, (255, 255, 255), (x_offset, y_offset, GRID_WIDTH*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE), 4)
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (x_offset, y_offset + i*BLOCK_SIZE), (x_offset + GRID_WIDTH*BLOCK_SIZE, y_offset + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (x_offset + j*BLOCK_SIZE, y_offset), (x_offset + j*BLOCK_SIZE, y_offset + GRID_HEIGHT*BLOCK_SIZE))

class PlayerState:
    def __init__(self, x_offset):
        self.locked_pos = {}
        self.grid = create_grid(self.locked_pos)
        self.change_piece = False
        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.fall_time = 0
        self.x_offset = x_offset
        self.score = 0
        self.lost = False

def main():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Three Player Tetris')
    
    players = [PlayerState(50), PlayerState(450), PlayerState(850)]
    clock = pygame.time.Clock()
    fall_speed = 0.27
    run = True

    while run:
        for player in players:
            if not player.lost:
                player.grid = create_grid(player.locked_pos)
                player.fall_time += clock.get_rawtime()

        clock.tick()

        for player in players:
            if not player.lost and player.fall_time / 1000 >= fall_speed:
                player.fall_time = 0
                player.current_piece.y += 1
                if not (valid_space(player.current_piece, player.grid)) and player.current_piece.y > 0:
                    player.current_piece.y -= 1
                    player.change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                
                if not players[0].lost:
                    if event.key == pygame.K_a:
                        players[0].current_piece.x -= 1
                        if not valid_space(players[0].current_piece, players[0].grid): players[0].current_piece.x += 1
                    if event.key == pygame.K_d:
                        players[0].current_piece.x += 1
                        if not valid_space(players[0].current_piece, players[0].grid): players[0].current_piece.x -= 1
                    if event.key == pygame.K_s:
                        players[0].current_piece.y += 1
                        if not valid_space(players[0].current_piece, players[0].grid): players[0].current_piece.y -= 1
                    if event.key == pygame.K_w:
                        players[0].current_piece.rotation += 1
                        if not valid_space(players[0].current_piece, players[0].grid): players[0].current_piece.rotation -= 1

                
                if not players[1].lost:
                    if event.key == pygame.K_LEFT:
                        players[1].current_piece.x -= 1
                        if not valid_space(players[1].current_piece, players[1].grid): players[1].current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        players[1].current_piece.x += 1
                        if not valid_space(players[1].current_piece, players[1].grid): players[1].current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        players[1].current_piece.y += 1
                        if not valid_space(players[1].current_piece, players[1].grid): players[1].current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        players[1].current_piece.rotation += 1
                        if not valid_space(players[1].current_piece, players[1].grid): players[1].current_piece.rotation -= 1

                
                if not players[2].lost:
                    if event.key == pygame.K_j:
                        players[2].current_piece.x -= 1
                        if not valid_space(players[2].current_piece, players[2].grid): players[2].current_piece.x += 1
                    if event.key == pygame.K_l:
                        players[2].current_piece.x += 1
                        if not valid_space(players[2].current_piece, players[2].grid): players[2].current_piece.x -= 1
                    if event.key == pygame.K_k:
                        players[2].current_piece.y += 1
                        if not valid_space(players[2].current_piece, players[2].grid): players[2].current_piece.y -= 1
                    if event.key == pygame.K_i:
                        players[2].current_piece.rotation += 1
                        if not valid_space(players[2].current_piece, players[2].grid): players[2].current_piece.rotation -= 1

        for player in players:
            if not player.lost:
                shape_pos = convert_shape_format(player.current_piece)
                for i in range(len(shape_pos)):
                    x, y = shape_pos[i]
                    if y > -1:
                        player.grid[y][x] = player.current_piece.color

                if player.change_piece:
                    for pos in shape_pos:
                        p = (pos[0], pos[1])
                        player.locked_pos[p] = player.current_piece.color
                    player.current_piece = player.next_piece
                    player.next_piece = get_shape()
                    player.change_piece = False
                    player.score += clear_rows(player.grid, player.locked_pos) * 10
                    if check_lost(player.locked_pos):
                        player.lost = True

        win.fill((0, 0, 0))
        font = pygame.font.SysFont('comicsans', 30)
        
        for i, player in enumerate(players):
            draw_grid(win, player.grid, player.x_offset, 100)
            label = font.render(f'Player {i+1} Score: {player.score}', 1, (255, 255, 255))
            win.blit(label, (player.x_offset, 50))
            if player.lost:
                lost_label = font.render('GAME OVER', 1, (255, 0, 0))
                win.blit(lost_label, (player.x_offset + 30, 350))

        pygame.display.update()

if __name__ == '__main__':
    main()