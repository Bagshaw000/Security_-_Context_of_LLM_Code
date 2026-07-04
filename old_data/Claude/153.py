import random

class Tetris:
    def __init__(self):
        self.players = [Player(i) for i in range(3)]
        self.board = Board()
        self.current_shapes = [player.get_new_shape() for player in self.players]
        self.game_over = False

    def play(self):
        while not self.game_over:
            for player in self.players:
                player.move_shape(self.board)
                if self.board.check_collision(player.shape, player.x, player.y):
                    self.board.add_shape(player.shape, player.x, player.y)
                    player.shape = player.get_new_shape()
                    if self.board.check_game_over(player.shape, player.x, player.y):
                        self.game_over = True
                        break
                self.board.update_board()

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.shape = None
        self.x = 0
        self.y = 0

    def get_new_shape(self):
        self.shape = Shape()
        self.x = 3
        self.y = 0
        return self.shape

    def move_shape(self, board):
        key = input(f"Player {self.player_id}, press a key: ")
        if key == "a":
            self.x -= 1
        elif key == "d":
            self.x += 1
        elif key == "s":
            self.y += 1
        elif key == "w":
            self.shape.rotate()
        if board.check_collision(self.shape, self.x, self.y):
            if key == "a":
                self.x += 1
            elif key == "d":
                self.x -= 1
            elif key == "s":
                self.y -= 1

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]

    def add_shape(self, shape, x, y):
        for row in range(shape.height):
            for col in range(shape.width):
                if shape.grid[row][col] == 1:
                    self.grid[y + row][x + col] = 1

    def update_board(self):
        for y in range(19, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(10)])

    def check_collision(self, shape, x, y):
        for row in range(shape.height):
            for col in range(shape.width):
                if shape.grid[row][col] == 1:
                    if y + row >= 20 or x + col < 0 or x + col >= 10 or self.grid[y + row][x + col] == 1:
                        return True
        return False

    def check_game_over(self, shape, x, y):
        for row in range(shape.height):
            for col in range(shape.width):
                if shape.grid[row][col] == 1 and y + row < 0:
                    return True
        return False

class Shape:
    def __init__(self):
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [1, 1, 1]]
        ]
        self.shape_index = random.randint(0, len(self.shapes) - 1)
        self.grid = self.shapes[self.shape_index]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def rotate(self):
        self.grid = list(map(list, zip(*self.grid[::-1])))
        self.width = len(self.grid[0])
        self.height = len(self.grid)

game = Tetris()
game.play()