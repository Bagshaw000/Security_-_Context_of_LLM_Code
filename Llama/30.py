import random
import time

class TetrisGame:
    def __init__(self):
        self.board = [[' ' for _ in range(10)] for _ in range(20)]
        self.shape_types = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        self.color_map = {'I': 'blue', 'J': 'red', 'L': 'green', 'O': 'yellow', 'S': 'purple', 'T': 'orange', 'Z': 'pink'}
        self.score = 0

    def generate_random_shape(self):
        shape_type = random.choice(self.shape_types)
        return shape_type

    def draw_board(self):
        for row in self.board:
            print(' '.join(row))

    def update_board(self, shape_type):
        shape = {
            'I': [
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            'J': [
                [2, 0, 0],
                [3, 3, 0],
                [0, 4, 0]
            ],
            'L': [
                [3, 0, 0],
                [0, 2, 5],
                [6, 4, 7]
            ],
            'O': [
                [8, 8],
                [8, 8]
            ],
            'S': [
                [9, 5, 1],
                [3, 5, 0],
                [0, 2, 4]
            ],
            'T': [
                [6, 7, 0],
                [0, 4, 4],
                [8, 5, 1]
            ],
            'Z': [
                [7, 0, 3],
                [9, 4, 2],
                [0, 5, 6]
            ]
        }
        shape = shape[shape_type]

        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val != 0:
                    self.board[y + 10 - len(shape)][x] = val

    def is_valid_move(self, shape_type):
        shape = {
            'I': [
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            'J': [
                [2, 0, 0],
                [3, 3, 0],
                [0, 4, 0]
            ],
            'L': [
                [3, 0, 0],
                [0, 2, 5],
                [6, 4, 7]
            ],
            'O': [
                [8, 8],
                [8, 8]
            ],
            'S': [
                [9, 5, 1],
                [3, 5, 0],
                [0, 2, 4]
            ],
            'T': [
                [6, 7, 0],
                [0, 4, 4],
                [8, 5, 1]
            ],
            'Z': [
                [7, 0, 3],
                [9, 4, 2],
                [0, 5, 6]
            ]
        }
        shape = shape[shape_type]

        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val != 0:
                    if self.board[y + 10 - len(shape)][x] != ' ':
                        return False
        return True

    def check_collision(self, shape_type):
        shape = {
            'I': [
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            'J': [
                [2, 0, 0],
                [3, 3, 0],
                [0, 4, 0]
            ],
            'L': [
                [3, 0, 0],
                [0, 2, 5],
                [6, 4, 7]
            ],
            'O': [
                [8, 8],
                [8, 8]
            ],
            'S': [
                [9, 5, 1],
                [3, 5, 0],
                [0, 2, 4]
            ],
            'T': [
                [6, 7, 0],
                [0, 4, 4],
                [8, 5, 1]
            ],
            'Z': [
                [7, 0, 3],
                [9, 4, 2],
                [0, 5, 6]
            ]
        }
        shape = shape[shape_type]

        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val != 0:
                    if self.board[y + 10 - len(shape)][x] != ' ':
                        return True
        return False

    def play(self):
        print("Welcome to Tetris!")
        while True:
            shape_type = self.generate_random_shape()
            self.update_board(shape_type)
            print("Your current score is:", self.score)
            time.sleep(1)  
            response = input("Press Enter to drop down the next piece, or Ctrl+C to quit. ")
            if 'Ctrl' in str(response):
                break
        self.draw_board()
        print("Game over! Final score:", self.score)

game = TetrisGame()
game.play()