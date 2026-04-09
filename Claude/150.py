import random

class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.players = [Player() for _ in range(3)]
        self.current_player = 0
        self.game_over = False

    def rotate_piece(self, piece, direction):
        if direction == 'left':
            piece = [list(reversed(col)) for col in zip(*piece)]
        else:
            piece = [list(reversed(row)) for row in zip(*piece[::-1])]
        return piece

    def check_collision(self, player, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j] and (y + i < 0 or y + i >= 20 or x + j < 0 or x + j >= 10 or self.board[y + i][x + j]):
                    return True
        return False

    def add_piece(self, player, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    self.board[y + i][x + j] = player.color

    def clear_lines(self):
        lines_cleared = 0
        for y in range(19, -1, -1):
            if all(self.board[y]):
                self.board.pop(y)
                self.board.insert(0, [0] * 10)
                lines_cleared += 1
        return lines_cleared

    def game_loop(self):
        while not self.game_over:
            player = self.players[self.current_player]
            piece = player.next_piece
            x, y = 4, 0

            while True:
                self.add_piece(player, piece, x, y)
                self.display_board()

                if self.check_collision(player, piece, x, y + 1):
                    self.add_piece(player, piece, x, y)
                    lines_cleared = self.clear_lines()
                    player.score += lines_cleared * 100
                    player.next_piece = random.choice(player.pieces)
                    self.current_player = (self.current_player + 1) % 3
                    break

                self.remove_piece(player, piece, x, y)
                y += 1

    def remove_piece(self, player, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    self.board[y + i][x + j] = 0

    def display_board(self):
        for row in self.board:
            print(''.join(['
        print()

class Player:
    def __init__(self):
        self.pieces = [
            [[1, 1, 1, 1]],
            [[1, 0], [1, 0], [1, 0], [1, 0]],
            [[0, 1, 0], [1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]]
        ]
        self.next_piece = random.choice(self.pieces)
        self.color = random.randint(1, 6)
        self.score = 0

game = Tetris()
game.game_loop()