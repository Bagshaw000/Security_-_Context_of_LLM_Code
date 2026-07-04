```python
import random
import time

class Tetris:
    def __init__(self, player1, player2, player3):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 0], [1, 0], [1, 1]],
            [[0, 1], [1, 1], [1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]]
        ]
        self.current_shape = random.choice(self.shapes)
        self.current_x = 3
        self.current_y = 0
        self.game_over = False

    def rotate_shape(self):
        self.current_shape = [list(reversed(col)) for col in zip(*self.current_shape)]

    def move_left(self):
        if self.check_valid_move(-1, 0):
            self.current_x -= 1

    def move_right(self):
        if self.check_valid_move(1, 0):
            self.current_x += 1

    def move_down(self):
        if self.check_valid_move(0, 1):
            self.current_y += 1
        else:
            self.lock_shape()

    def check_valid_move(self, dx, dy):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                new_x = self.current_x + x + dx
                new_y = self.current_y + y + dy
                if new_x < 0 or new_x >= 10 or new_y >= 20 or (new_y >= 0 and self.board[new_y][new_x]):
                    return False
        return True

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                new_x = self.current_x + x
                new_y = self.current_y + y
                if new_y >= 0:
                    self.board[new_y][new_x] = cell
        self.clear_lines()
        self.current_shape = random.choice(self.shapes)
        self.current_x = 3
        self.current_y = 0
        if not self.check_valid_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        rows_to_remove = []
        for y in range(20):
            if all(self.board[y]):
                rows_to_remove.append(y)
        if rows_to_remove:
            for y in rows_to_remove:
                self.board.pop(y)
                self.board.insert(0, [0] * 10)

    def play(self):
        while not self.game_over:
            self.player1.make_move(self)
            self.player2.make_move(self)
            self.player3.make_move(self)
            time.sleep(0.1)

class Player:
    def __init__(self, name):
        self.name = name

    def make_move(self, game):
        pass

class RandomPlayer(Player):
    def make_move(self, game):
        move = random.choice(['left', 'right', 'rotate', 'down'])
        if move == 'left':
            game.move_left()
        elif move == 'right':
            game.move_right()
        elif move == 'rotate':
            game.rotate_shape()
        elif move == 'down':
            game.move_down()

class HumanPlayer(Player):
    def make_move(self, game):
        while True:
            move = input(f"{self.name}'s move (left, right, rotate, down): ")
            if move == 'left':
                game.move_left()
                break
            elif move == 'right':
                game.move_right()
                break
            elif move == 'rotate':
                game.rotate_shape()
                break
            elif move == 'down':
                game.move_down()
                break
            else:
                print("Invalid move. Please try again.")


player1 = HumanPlayer("John")
player2 = RandomPlayer("Player 2")
player3 = RandomPlayer("Player 3")
game = Tetris(player1, player2, player3)
game.play()
```