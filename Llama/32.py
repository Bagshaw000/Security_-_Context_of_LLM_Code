import random
import time

class Shape:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.blocks = [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ]

    def rotate(self):
        for i in range(3):
            for j in range(3):
                if self.blocks[j][i] == 1:
                    if i < 2 and self.blocks[i+1][j] == 1:
                        return
                    elif j < 2 and self.blocks[i][j+1] == 1:
                        return
                    else:
                        self.blocks = [row[::-1] for row in self.blocks]

class Tetris:
    def __init__(self):
        self.board = [[0]*10 for _ in range(20)]
        self.shapes = [
            Shape(),
            Shape(),
            Shape(),
            Shape()
        ]
        self.current_shape_index = 0
        self.speed = 1

    def drop_shape(self):
        shape = self.shapes[self.current_shape_index]
        while True:
            new_y = shape.y + len(shape.blocks)
            if all([self.board[new_y][new_x] != 1 for new_x in range(10)]):
                break
            time.sleep(0.5)
            shape.y += 1

    def rotate_shape(self, shape):
        shape.rotate()
        if not all([all([self.board[y][x] == 1 for x in range(10)]) for y in range(len(shape.blocks))]):
            shape = Shape()

    def place_shape_on_board(self, shape):
        new_y = len(shape.blocks)
        for i, block_row in enumerate(shape.blocks):
            for j, block in enumerate(block_row):
                if block == 1:
                    self.board[new_y+i][j+self.x] = 1

    def check_rows(self):
        for y in range(len(self.board)-1):
            row = [x for x in self.board[y]]
            if all([row[i] != 0 for i in range(10)]):
                return y
        return None

    def clear_rows(self, cleared_row_y):
        rows_to_clear = set()
        for y in range(cleared_row_y-1, -1, -1):
            row = [x for x in self.board[y]]
            if all([row[i] != 0 for i in range(10)]):
                rows_to_clear.add(y)
            else:
                break
        to_remove = []
        for y in sorted(rows_to_clear, reverse=True):
            line_y = max(y, cleared_row_y) + 1
            row = [x for x in self.board[line_y]]
            for i in range(10):
                if row[i] == 0:
                    break
                to_remove.append(line_y)
        for y in sorted(to_remove, reverse=True):
            del self.board[y]

    def run(self):
        while True:
            self.drop_shape()
            cleared_row_y = self.check_rows()
            if cleared_row_y is not None:
                self.clear_rows(cleared_row_y)
            self.current_shape_index += 1
            self.speed += 0.05

if __name__ == "__main__":
    game = Tetris()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.x -= 1
                elif event.key == pygame.K_RIGHT:
                    game.x += 1
        game.run()