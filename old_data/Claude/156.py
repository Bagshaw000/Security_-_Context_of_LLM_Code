import random

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.position = [0, 3]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def move(self, dx, dy):
        self.position[0] += dy
        self.position[1] += dx

class TetrisBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.current_tetrominos = [Tetromino(random.choice(tetromino_shapes), random.choice(tetromino_colors)) for _ in range(3)]

    def check_collision(self, tetromino):
        for y, row in enumerate(tetromino.shape[tetromino.rotation]):
            for x, cell in enumerate(row):
                if cell and (tetromino.position[0] + y < 0 or tetromino.position[0] + y >= self.height or tetromino.position[1] + x < 0 or tetromino.position[1] + x >= self.width or self.board[tetromino.position[0] + y][tetromino.position[1] + x]):
                    return True
        return False

    def update(self):
        for i, tetromino in enumerate(self.current_tetrominos):
            tetromino.move(0, 1)
            if self.check_collision(tetromino):
                tetromino.move(0, -1)
                for y, row in enumerate(tetromino.shape[tetromino.rotation]):
                    for x, cell in enumerate(row):
                        if cell:
                            self.board[tetromino.position[0] + y][tetromino.position[1] + x] = tetromino.color
                self.current_tetrominos[i] = Tetromino(random.choice(tetromino_shapes), random.choice(tetromino_colors))

    def draw(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print()
        for tetromino in self.current_tetrominos:
            for y, row in enumerate(tetromino.shape[tetromino.rotation]):
                line = [' '] * self.width
                for x, cell in enumerate(row):
                    if cell:
                        line[tetromino.position[1] + x] = tetromino.color
                print(' '.join(line))
            print()

tetromino_shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0], [1, 1], [0, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1], [1, 1], [1, 0]]
]

tetromino_colors = ['R', 'G', 'B', 'Y', 'C', 'M', 'W']

board = TetrisBoard(10, 20)

while True:
    board.update()
    board.draw()