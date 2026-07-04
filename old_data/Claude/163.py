import random

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.position = [4, 0]

    def move_left(self, board):
        self.position[0] -= 1
        if not self.valid_position(board):
            self.position[0] += 1

    def move_right(self, board):
        self.position[0] += 1
        if not self.valid_position(board):
            self.position[0] -= 1

    def move_down(self, board):
        self.position[1] += 1
        if not self.valid_position(board):
            self.position[1] -= 1
            return True
        return False

    def rotate(self, board):
        self.rotation = (self.rotation + 1) % len(self.shape)
        if not self.valid_position(board):
            self.rotation = (self.rotation - 1) % len(self.shape)

    def valid_position(self, board):
        for y in range(len(self.shape[self.rotation])):
            for x in range(len(self.shape[self.rotation][y])):
                if self.shape[self.rotation][y][x] and (
                    self.position[0] + x < 0
                    or self.position[0] + x >= 10
                    or self.position[1] + y >= 20
                    or board[self.position[1] + y][self.position[0] + x]
                ):
                    return False
        return True

class TetrisGame:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.players = [
            Tetromino(random.choice(tetromino_shapes)),
            Tetromino(random.choice(tetromino_shapes)),
            Tetromino(random.choice(tetromino_shapes)),
        ]
        self.current_player = 0

    def update(self):
        player = self.players[self.current_player]
        if player.move_down(self.board):
            self.lock_piece(player)
            self.clear_lines()
            self.current_player = (self.current_player + 1) % 3
            self.players[self.current_player] = Tetromino(random.choice(tetromino_shapes))

    def lock_piece(self, player):
        for y in range(len(player.shape[player.rotation])):
            for x in range(len(player.shape[player.rotation][y])):
                if player.shape[player.rotation][y][x]:
                    self.board[player.position[1] + y][player.position[0] + x] = 1

    def clear_lines(self):
        lines_cleared = 0
        for y in range(19, -1, -1):
            if all(self.board[y]):
                self.board.pop(y)
                self.board.insert(0, [0 for _ in range(10)])
                lines_cleared += 1
        return lines_cleared

tetromino_shapes = [
    [
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ],
    [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ],
    [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ],
    [
        [1, 1],
        [1, 1],
    ],
    [
        [1, 1, 1],
        [0, 1, 0],
        [0, 0, 0],
    ],
]

game = TetrisGame()

while True:
    game.update()