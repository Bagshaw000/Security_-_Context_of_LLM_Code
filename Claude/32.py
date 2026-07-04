import random

class TetrisGame:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.players = ["Player 1", "Player 2", "Player 3"]
        self.scores = [0, 0, 0]
        self.current_player = 0

    def print_board(self):
        for row in self.board:
            print(row)

    def check_lines(self):
        for row in range(19, -1, -1):
            if 0 not in self.board[row]:
                self.board.pop(row)
                self.board.insert(0, [0 for _ in range(10)])
                self.scores[self.current_player] += 10

    def move_piece(self, piece, direction):
        
        pass

    def rotate_piece(self, piece):
        
        pass

    def place_piece(self, piece):
        
        pass

    def game_loop(self):
        while True:
            self.print_board()
            print(f"Current player: {self.players[self.current_player]}")
            print(f"Score: {self.scores[self.current_player]}")

            
            move = input("Enter move (left, right, down, rotate): ")

            
            if move == "left":
                self.move_piece(piece, "left")
            elif move == "right":
                self.move_piece(piece, "right")
            elif move == "down":
                self.move_piece(piece, "down")
            elif move == "rotate":
                self.rotate_piece(piece)
            else:
                print("Invalid move, try again.")

            
            self.check_lines()

            
            self.current_player = (self.current_player + 1) % 3

            
            piece = self.generate_piece()

            
            self.place_piece(piece)

    def generate_piece(self):
        
        pass

game = TetrisGame()
game.game_loop()