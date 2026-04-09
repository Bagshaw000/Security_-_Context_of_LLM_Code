import random

class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 1, 1], [0, 1, 0]]
        ]
        self.current_shapes = [random.choice(self.shapes) for _ in range(3)]
        self.positions = [(0, 4), (0, 3), (0, 2)]
        self.scores = [0, 0, 0]

    def rotate(self, player):
        shape = self.current_shapes[player]
        self.current_shapes[player] = [list(reversed(col)) for col in zip(*shape)]

    def move(self, player, direction):
        x, y = self.positions[player]
        shape = self.current_shapes[player]
        if direction == 'left':
            new_y = y - 1
        else:
            new_y = y + 1
        if new_y >= 0 and new_y + len(shape[0]) <= 10 and all(self.board[x+i][new_y+j] == 0 for i in range(len(shape)) for j in range(len(shape[0]))):
            self.positions[player] = (x, new_y)

    def drop(self, player):
        x, y = self.positions[player]
        shape = self.current_shapes[player]
        while x + len(shape) <= 20 and all(self.board[x+i][y+j] == 0 for i in range(len(shape)) for j in range(len(shape[0]))):
            x += 1
        x -= 1
        self.positions[player] = (x, y)
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    self.board[x+i][y+j] = 1
        self.current_shapes[player] = random.choice(self.shapes)
        self.positions[player] = (0, 4)
        self.check_lines()

    def check_lines(self):
        for i in range(19, -1, -1):
            if all(self.board[i][j] == 1 for j in range(10)):
                for j in range(10):
                    self.board[i][j] = 0
                for k in range(i, 0, -1):
                    for j in range(10):
                        self.board[k][j] = self.board[k-1][j]
                self.scores[0] += 1
                self.scores[1] += 1
                self.scores[2] += 1

    def play(self):
        while True:
            for player in range(3):
                print(f"Player {player+1}'s turn:")
                for row in self.board:
                    print(row)
                print(f"Score: {self.scores[player]}")
                print(f"Current shape: {self.current_shapes[player]}")
                print("Actions: 'rotate', 'left', 'right', 'drop'")
                action = input("Enter an action: ")
                if action == 'rotate':
                    self.rotate(player)
                elif action == 'left':
                    self.move(player, 'left')
                elif action == 'right':
                    self.move(player, 'right')
                elif action == 'drop':
                    self.drop(player)

game = Tetris()
game.play()