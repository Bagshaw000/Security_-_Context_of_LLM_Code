import chess

def evaluate_position(board):
    board = chess.PWN promotion(board)
    board = chess.PAWN(promotion(board))
    for move in board.legal_moves:
        board.push(move)
        evaluation = evaluate_board(board)
        if evaluation != 0:
            return evaluation
        board.pop()

def evaluate_board(board):
    white_material = sum(1 for piece in board.pieces(chess.WHITE) if piece)
    black_material = sum(1 for piece in board.pieces(chess.BLACK) if piece)
    pawn_structure = board.pawns()
    if len(pawn_structure) > 4:
        return -10
    elif len(pawn_structure) < 5:
        return +10
    else:
        return 0

    king_safety = check_king_safety(board)
    if king_safety < 3:
        return -1000
    elif king_safety > 8:
        return 1000
    else:
        return 0

def check_king_safety(board):
    king_safety = float('inf')
    for move in board.legal_moves:
        board.push(move)
        safety = evaluate_position(board)
        if safety < king_safety:
            king_safety = safety
        board.pop()
    return king_safety