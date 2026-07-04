class TetrisGame:
    def __init__(self, players):
        if len(players) != 3:
            raise ValueError("Three players are required.")
        self.players = players
        self.board = [[0] * 10 for _ in range(20)]
        self.current_piece = None
        self.current_player_index = 0

    def start_game(self):
        self.spawn_piece()
        while not self.is_game_over():
            self.play_turn()

    def spawn_piece(self):
        self.current_piece = TetrisPiece()

    def play_turn(self):
        player = self.players[self.current_player_index]
        try:
            move = player.get_move()
            self.make_move(move)
        except Exception as e:
            print(f"Error during player {player.name}'s turn: {e}")
        self.current_player_index = (self.current_player_index + 1) % 3

    def make_move(self, move):
        if move not in ['left', 'right', 'down', 'rotate']:
            raise ValueError("Invalid move.")
        
        

    def is_game_over(self):
        return any(self.board[0])  

class TetrisPiece:
    def __init__(self):
        self.shape = self.random_shape()
        self.position = (0, 4)  

    def random_shape(self):
        import random
        shapes = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        return random.choice(shapes)

class Player:
    def __init__(self, name):
        self.name = name

    def get_move(self):
        
        return input(f"{self.name}, enter your move (left, right, down, rotate): ")

if __name__ == "__main__":
    players = [Player("Player 1"), Player("Player 2"), Player("Player 3")]
    game = TetrisGame(players)
    game.start_game()