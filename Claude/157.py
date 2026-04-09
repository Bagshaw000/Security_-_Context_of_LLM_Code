import random

class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.players = [[], [], []]
        self.piece_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        self.player_scores = [0, 0, 0]

    def get_random_piece(self):
        return random.choice(self.piece_types)

    def check_full_rows(self, player_index):
        full_rows = []
        for row in range(20):
            if all(self.board[row]):
                full_rows.append(row)
        if full_rows:
            for row in sorted(full_rows, reverse=True):
                del self.board[row]
                self.board.insert(0, [0] * 10)
            self.player_scores[player_index] += len(full_rows) * 100

    def rotate_piece(self, piece, direction):
        if piece == 'I':
            if direction == 'clockwise':
                return ['I', 'I', 'I', 'I']
            else:
                return ['I', 'I', 'I', 'I']
        elif piece == 'O':
            return ['O', 'O', 'O', 'O']
        elif piece == 'T':
            if direction == 'clockwise':
                return ['T', 'T', 'T', '_']
            else:
                return ['_', 'T', 'T', 'T']
        elif piece == 'S':
            if direction == 'clockwise':
                return ['_', 'S', 'S', 'S']
            else:
                return ['S', 'S', '_', 'S']
        elif piece == 'Z':
            if direction == 'clockwise':
                return ['Z', 'Z', '_', 'Z']
            else:
                return ['_', 'Z', 'Z', 'Z']
        elif piece == 'J':
            if direction == 'clockwise':
                return ['J', '_', '_', 'J']
            else:
                return ['_', 'J', 'J', 'J']
        elif piece == 'L':
            if direction == 'clockwise':
                return ['_', '_', 'L', 'L']
            else:
                return ['L', 'L', 'L', '_']

    def place_piece(self, player_index, piece, x, y):
        if piece == 'I':
            self.players[player_index].extend([(x, y), (x, y + 1), (x, y + 2), (x, y + 3)])
        elif piece == 'O':
            self.players[player_index].extend([(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)])
        elif piece == 'T':
            self.players[player_index].extend([(x, y), (x - 1, y), (x + 1, y), (x, y + 1)])
        elif piece == 'S':
            self.players[player_index].extend([(x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 2, y)])
        elif piece == 'Z':
            self.players[player_index].extend([(x, y), (x + 1, y), (x + 1, y + 1), (x + 2, y + 1)])
        elif piece == 'J':
            self.players[player_index].extend([(x, y), (x, y + 1), (x, y + 2), (x + 1, y + 2)])
        elif piece == 'L':
            self.players[player_index].extend([(x, y), (x, y + 1), (x, y + 2), (x - 1, y + 2)])

        for x, y in self.players[player_index]:
            self.board[y][x] = 1

        self.check_full_rows(player_index)

    def run_game(self):
        while True:
            for player_index in range(3):
                piece = self.get_random_piece()
                x = random.randint(0, 6)
                y = 0
                self.place_piece(player_index, piece, x, y)
                print(f"Player {player_index + 1} placed a {piece} piece at ({x}, {y})")
                print(f"Player {player_index + 1} score: {self.player_scores[player_index]}")

if __name__ == "__main__":
    game = Tetris()
    game.run_game()