class ChessPosition:
    def __init__(self):
        self.board = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.white_pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
        self.black_pieces = ['p', 'r', 'n', 'b', 'q', 'k']

    def evaluate(self):
        white_score = 0
        black_score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece in self.white_pieces:
                    white_score += self.get_piece_value(piece)
                elif piece in self.black_pieces:
                    black_score += self.get_piece_value(piece)
        return white_score - black_score

    def get_piece_value(self, piece):
        if piece == 'p' or piece == 'P':
            return 1
        elif piece == 'n' or piece == 'N':
            return 3
        elif piece == 'b' or piece == 'B':
            return 3
        elif piece == 'r' or piece == 'R':
            return 5
        elif piece == 'q' or piece == 'Q':
            return 9
        elif piece == 'k' or piece == 'K':
            return 0
        else:
            return 0

position = ChessPosition()
print(position.evaluate())