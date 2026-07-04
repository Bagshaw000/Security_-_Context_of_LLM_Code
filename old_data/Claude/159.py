import random

class Tetris:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.players = [Player(self) for _ in range(3)]
        self.current_player = 0

    def rotate_piece(self, player, direction):
        player.current_piece.rotate(direction)
        if not self.check_valid_position(player):
            player.current_piece.rotate(-direction)

    def move_piece(self, player, dx, dy):
        player.current_piece.move(dx, dy)
        if not self.check_valid_position(player):
            player.current_piece.move(-dx, -dy)

    def check_valid_position(self, player):
        for x, y in player.current_piece.get_positions():
            if x < 0 or x >= self.width or y < 0 or y >= self.height or self.board[y][x] != 0:
                return False
        return True

    def place_piece(self, player):
        for x, y in player.current_piece.get_positions():
            self.board[y][x] = player.color
        player.score += player.current_piece.score
        player.current_piece = player.next_piece
        player.next_piece = Piece(random.choice(Piece.SHAPES), player.color)

    def clear_lines(self):
        lines_cleared = 0
        for y in range(self.height):
            if all(self.board[y]):
                self.board.pop(y)
                self.board.insert(0, [0] * self.width)
                lines_cleared += 1
        return lines_cleared

    def play_turn(self):
        player = self.players[self.current_player]
        self.rotate_piece(player, 0)
        self.move_piece(player, 0, -1)
        if not self.check_valid_position(player):
            self.place_piece(player)
            lines_cleared = self.clear_lines()
            player.score += lines_cleared * 100
            self.current_player = (self.current_player + 1) % len(self.players)

class Player:
    def __init__(self, game):
        self.game = game
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        self.score = 0
        self.current_piece = Piece(random.choice(Piece.SHAPES), self.color)
        self.next_piece = Piece(random.choice(Piece.SHAPES), self.color)

class Piece:
    SHAPES = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],  
        [(0, 0), (0, 1), (1, 0), (1, 1)],  
        [(0, 0), (1, 0), (2, 0), (2, 1)],  
        [(0, 0), (1, 0), (1, 1), (2, 1)],  
        [(0, 0), (0, 1), (1, 1), (2, 1)],  
        [(0, 1), (1, 0), (1, 1), (2, 0)],  
        [(0, 0), (1, 0), (1, 1), (2, 0)]   
    ]

    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.score = 0

    def rotate(self, direction):
        self.rotation = (self.rotation + direction) % 4
        self.shape = [(-y, x) for x, y in self.shape]

    def move(self, dx, dy):
        self.shape = [(x + dx, y + dy) for x, y in self.shape]

    def get_positions(self):
        return self.shape