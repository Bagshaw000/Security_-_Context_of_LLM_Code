import random
import time

class TetrisBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for x in range(width)] for y in range(height)]

    def add_piece(self, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] == 1:
                    self.board[y+i][x+j] = 1

    def clear_line(self):
        lines_cleared = 0
        for y in range(self.height-1, -1, -1):
            if all(self.board[y]):
                self.board.pop(y)
                self.board.insert(0, [0 for x in range(self.width)])
                lines_cleared += 1
        return lines_cleared

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = 4
        self.y = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.board = TetrisBoard(10, 20)
        self.current_piece = Tetromino(random.choice(TETROMINO_SHAPES))

    def play_turn(self):
        print(f"{self.name}'s turn:")
        self.board.add_piece(self.current_piece.shape[self.current_piece.rotation], self.current_piece.x, self.current_piece.y)
        lines_cleared = self.board.clear_line()
        self.score += lines_cleared * 10
        print(f"Score: {self.score}")
        self.current_piece = Tetromino(random.choice(TETROMINO_SHAPES))

TETROMINO_SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[1, 1, 1], [0, 1, 0]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]]   
]

def main():
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    player3 = Player("Player 3")

    while True:
        player1.play_turn()
        player2.play_turn()
        player3.play_turn()
        time.sleep(1)

if __name__ == "__main__":
    main()