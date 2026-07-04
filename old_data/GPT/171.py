class ChessPositionEvaluator:
    def __init__(self):
        self.piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0
        }

    def evaluate_position(self, board):
        score = 0
        for row in board:
            for piece in row:
                score += self.piece_values.get(piece, 0)
        return score


board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

evaluator = ChessPositionEvaluator()
print(evaluator.evaluate_position(board))