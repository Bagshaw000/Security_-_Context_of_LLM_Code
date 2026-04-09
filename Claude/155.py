import random

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

class Player:
    def __init__(self, board_width, board_height):
        self.board = [[0 for _ in range(board_width)] for _ in range(board_height)]
        self.current_piece = None
        self.score = 0

    def add_piece(self, piece):
        self.current_piece = piece

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_down(self):
        pass

    def rotate_piece(self):
        pass

    def check_for_lines(self):
        pass

    def update_score(self, lines_cleared):
        pass

class Game:
    def __init__(self, board_width, board_height):
        self.players = [Player(board_width, board_height) for _ in range(3)]
        self.piece_pool = [Piece([[1, 1, 1, 1]], (0, 255, 0)),
                          Piece([[1, 1], [1, 1]], (255, 0, 0)),
                          Piece([[0, 1, 1], [1, 1, 0]], (0, 0, 255)),
                          Piece([[1, 1, 0], [0, 1, 1]], (255, 255, 0)),
                          Piece([[1, 0, 0], [1, 1, 1]], (255, 0, 255)),
                          Piece([[0, 0, 1], [1, 1, 1]], (0, 255, 255)),
                          Piece([[1, 1, 1], [0, 1, 0]], (128, 128, 128))]

    def start(self):
        while True:
            for player in self.players:
                self.add_new_piece(player)
                while True:
                    self.handle_input(player)
                    if self.check_game_over(player):
                        break
                    self.update_board(player)
            self.clear_lines()
            self.update_scores()

    def add_new_piece(self, player):
        piece = random.choice(self.piece_pool)
        player.add_piece(piece)

    def handle_input(self, player):
        pass

    def check_game_over(self, player):
        pass

    def update_board(self, player):
        pass

    def clear_lines(self):
        pass

    def update_scores(self):
        pass

game = Game(10, 20)
game.start()