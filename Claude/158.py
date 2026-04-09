import random

class Tetris:
    def __init__(self, players):
        self.players = players
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.pieces = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]]
        ]
        self.current_pieces = [random.choice(self.pieces) for _ in range(3)]

    def rotate_piece(self, player_idx, clockwise=True):
        piece = self.current_pieces[player_idx]
        if clockwise:
            piece = list(map(list, zip(*piece[::-1])))
        else:
            piece = list(map(list, zip(*piece)))[::-1]
        self.current_pieces[player_idx] = piece

    def move_piece(self, player_idx, dx, dy):
        piece = self.current_pieces[player_idx]
        x, y = self.find_piece_position(player_idx)
        new_x, new_y = x + dx, y + dy
        if self.check_valid_move(player_idx, new_x, new_y):
            self.clear_piece(player_idx, x, y)
            self.draw_piece(player_idx, new_x, new_y)
            return True
        return False

    def find_piece_position(self, player_idx):
        piece = self.current_pieces[player_idx]
        for y in range(len(self.board) - len(piece) + 1):
            for x in range(len(self.board[0]) - len(piece[0]) + 1):
                if self.check_valid_move(player_idx, x, y):
                    return x, y
        return None, None

    def check_valid_move(self, player_idx, x, y):
        piece = self.current_pieces[player_idx]
        for dy, row in enumerate(piece):
            for dx, cell in enumerate(row):
                if cell and (y + dy >= len(self.board) or x + dx >= len(self.board[0]) or self.board[y + dy][x + dx]):
                    return False
        return True

    def clear_piece(self, player_idx, x, y):
        piece = self.current_pieces[player_idx]
        for dy, row in enumerate(piece):
            for dx, cell in enumerate(row):
                if cell:
                    self.board[y + dy][x + dx] = 0

    def draw_piece(self, player_idx, x, y):
        piece = self.current_pieces[player_idx]
        for dy, row in enumerate(piece):
            for dx, cell in enumerate(row):
                if cell:
                    self.board[y + dy][x + dx] = player_idx + 1

    def check_full_rows(self):
        to_remove = []
        for y in range(len(self.board)):
            if all(self.board[y]):
                to_remove.append(y)
        if to_remove:
            for y in reversed(to_remove):
                del self.board[y]
                self.board.insert(0, [0] * 10)
            return len(to_remove)
        return 0

    def play(self):
        while True:
            for player_idx, player in enumerate(self.players):
                x, y = self.find_piece_position(player_idx)
                if x is None:
                    self.players[player_idx].score += self.check_full_rows()
                    self.current_pieces[player_idx] = random.choice(self.pieces)
                else:
                    move_made = False
                    while not move_made:
                        action = player.get_action(self.board, self.current_pieces[player_idx], x, y)
                        if action == 'rotate':
                            self.rotate_piece(player_idx)
                            x, y = self.find_piece_position(player_idx)
                        elif action == 'left':
                            move_made = self.move_piece(player_idx, -1, 0)
                        elif action == 'right':
                            move_made = self.move_piece(player_idx, 1, 0)
                        elif action == 'down':
                            move_made = self.move_piece(player_idx, 0, 1)
                        elif action == 'drop':
                            while self.move_piece(player_idx, 0, 1):
                                pass
                            self.players[player_idx].score += self.check_full_rows()
                            self.current_pieces[player_idx] = random.choice(self.pieces)
                            move_made = True
                        else:
                            move_made = True
            self.check_full_rows()