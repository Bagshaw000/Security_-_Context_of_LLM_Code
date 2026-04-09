import random


shapes = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
    [[1, 1, 1], [0, 1, 0]]  
]


board_width = 10
board_height = 20


players = [
    {'board': [[0] * board_width for _ in range(board_height)], 'score': 0},
    {'board': [[0] * board_width for _ in range(board_height)], 'score': 0},
    {'board': [[0] * board_width for _ in range(board_height)], 'score': 0}
]

def rotate_shape(shape):
    return [list(reversed(col)) for col in zip(*shape)]

def check_collision(board, shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell and (y + i < 0 or y + i >= board_height or x + j < 0 or x + j >= board_width or board[y + i][x + j]):
                return True
    return False

def add_shape_to_board(board, shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                board[y + i][x + j] = 1

def clear_lines(board):
    lines_cleared = 0
    for y in range(board_height - 1, -1, -1):
        if all(cell == 1 for cell in board[y]):
            del board[y]
            board.insert(0, [0] * board_width)
            lines_cleared += 1
    return lines_cleared

def update_scores(players, lines_cleared):
    for player in players:
        player['score'] += lines_cleared ** 2

def game_loop():
    while True:
        for player in players:
            
            shape = random.choice(shapes)
            x = board_width // 2 - len(shape[0]) // 2
            y = 0

            while True:
                
                if check_collision(player['board'], shape, x, y + 1):
                    
                    add_shape_to_board(player['board'], shape, x, y)
                    lines_cleared = clear_lines(player['board'])
                    update_scores(players, lines_cleared)
                    break
                y += 1

                
                

                
                

game_loop()