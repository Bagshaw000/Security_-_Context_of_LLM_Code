import random


BOARD_WIDTH = 10
BOARD_HEIGHT = 20


PIECES = [
    [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]],
    [[0, 2, 2],
     [2, 2, 0],
     [0, 0, 0]],
    [[3, 3, 3, 3],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[4, 0, 0],
     [4, 4, 4],
     [0, 0, 0]],
    [[0, 5, 5],
     [5, 5, 0],
     [0, 0, 0]],
    [[6, 6, 0],
     [0, 6, 6],
     [0, 0, 0]],
    [[7, 7, 7],
     [0, 7, 0],
     [0, 0, 0]]
]


game_state = [[[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)] for z in range(3)]
player_scores = [0, 0, 0]
current_pieces = [None, None, None]
piece_positions = [[0, 0], [0, 0], [0, 0]]
piece_rotations = [0, 0, 0]


while True:
    
    for player in range(3):
        for y in range(BOARD_HEIGHT - 1, -1, -1):
            if all(game_state[player][y]):
                game_state[player].pop(y)
                game_state[player].insert(0, [0] * BOARD_WIDTH)
                player_scores[player] += 1

    
    for player in range(3):
        if current_pieces[player] is None:
            current_pieces[player] = random.choice(PIECES)
            piece_positions[player] = [0, 4]
            piece_rotations[player] = 0

        
        if piece_positions[player][0] < BOARD_HEIGHT - 1 and all(game_state[player][piece_positions[player][0] + 1][piece_positions[player][1]:piece_positions[player][1] + len(current_pieces[player][0])] == [0] * len(current_pieces[player][0])):
            piece_positions[player][0] += 1
        else:
            
            for y in range(len(current_pieces[player])):
                for x in range(len(current_pieces[player][y])):
                    if current_pieces[player][y][x]:
                        game_state[player][piece_positions[player][0] - len(current_pieces[player]) + y][piece_positions[player][1] + x] = current_pieces[player][y][x]
            current_pieces[player] = None

        
        if any(game_state[player][0]):
            print(f"Player {player + 1} has lost!")
            break