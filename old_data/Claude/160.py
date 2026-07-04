import random

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.orientation = 0
        self.x = 4
        self.y = 0

    def rotate(self):
        self.orientation = (self.orientation + 1) % len(self.shape)

    def move_left(self):
        self.x = max(self.x - 1, 0)

    def move_right(self):
        self.x = min(self.x + 1, 9)

    def move_down(self):
        self.y = min(self.y + 1, 19)

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]

    def add_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.shape[tetromino.orientation]):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[tetromino.y + y][tetromino.x + x] = cell

    def clear_lines(self):
        lines_cleared = 0
        for y in range(19, -1, -1):
            if all(self.grid[y]):
                self.grid.pop(y)
                self.grid.insert(0, [0] * 10)
                lines_cleared += 1
        return lines_cleared

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.board = Board()
        self.current_tetromino = None

    def spawn_tetromino(self):
        shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 0], [1, 0], [1, 1]],
            [[0, 1], [0, 1], [1, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 1], [0, 1, 0]]
        ]
        self.current_tetromino = Tetromino(random.choice(shapes))

    def update(self):
        self.board.add_tetromino(self.current_tetromino)
        lines_cleared = self.board.clear_lines()
        self.score += lines_cleared * 100
        self.spawn_tetromino()

def main():
    players = [Player("Player 1"), Player("Player 2"), Player("Player 3")]

    while True:
        for player in players:
            if not player.current_tetromino:
                player.spawn_tetromino()
            player.update()
            print(f"{player.name} score: {player.score}")
            for row in player.board.grid:
                print(row)
            print()

if __name__ == "__main__":
    main()