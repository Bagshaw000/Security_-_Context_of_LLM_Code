import random

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.position = (0, 4)
        self.orientation = 0

    def rotate(self, direction):
        self.orientation = (self.orientation + direction) % 4

    def move(self, direction):
        x, y = self.position
        if direction == 'left':
            self.position = (x, y - 1)
        elif direction == 'right':
            self.position = (x, y + 1)
        elif direction == 'down':
            self.position = (x + 1, y)

class Player:
    def __init__(self, name):
        self.name = name
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.current_tetromino = None
        self.score = 0

    def spawn_tetromino(self):
        shapes = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        self.current_tetromino = Tetromino(random.choice(shapes))

    def update_board(self):
        x, y = self.current_tetromino.position
        shape = self.current_tetromino.shape
        orientation = self.current_tetromino.orientation
        for i in range(4):
            for j in range(4):
                if shape[orientation][i][j] == 1:
                    self.board[x + i][y + j] = 1

    def check_lines(self):
        lines_cleared = 0
        for row in range(19, -1, -1):
            if all(self.board[row]):
                self.board.pop(row)
                self.board.insert(0, [0] * 10)
                lines_cleared += 1
        self.score += lines_cleared ** 2

def main():
    players = [Player('Player 1'), Player('Player 2'), Player('Player 3')]

    while True:
        for player in players:
            player.spawn_tetromino()
            while True:
                player.update_board()
                
                player.check_lines()
                break

if __name__ == '__main__':
    main()