import random

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
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.current_tetromino = None

    def spawn_tetromino(self):
        shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 0], [1, 0], [1, 1]],
            [[0, 1], [1, 1], [1, 0]]
        ]
        self.current_tetromino = Tetromino(random.choice(shapes))

    def update_board(self):
        for y in range(20):
            for x in range(10):
                if self.board[y][x] == 1:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

    def play_turn(self):
        while True:
            action = input(f"{self.name}'s turn: ").lower()
            if action == "rotate":
                self.current_tetromino.rotate()
            elif action == "left":
                self.current_tetromino.move_left()
            elif action == "right":
                self.current_tetromino.move_right()
            elif action == "down":
                self.current_tetromino.move_down()
            elif action == "quit":
                break
            self.update_board()

def main():
    players = [Player("Brad"), Player("Alice"), Player("Charlie")]

    while True:
        for player in players:
            player.spawn_tetromino()
            player.play_turn()

if __name__ == "__main__":
    main()