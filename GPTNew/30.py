import random
import json
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import unittest

app = Flask(__name__)
CORS(app)


s3 = boto3.client('s3')
BUCKET_NAME = 'your-bucket-name'


BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
]

class Game:
    def __init__(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.current_position = (0, 0)

    def new_piece(self):
        self.current_piece = random.choice(SHAPES)
        self.current_position = (0, BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2)

    def rotate_piece(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]

    def move_piece(self, direction):
        x, y = self.current_position
        if direction == 'left':
            self.current_position = (x, y - 1)
        elif direction == 'right':
            self.current_position = (x, y + 1)
        elif direction == 'down':
            self.current_position = (x + 1, y)

    def lock_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, value in enumerate(row):
                if value:
                    self.board[self.current_position[0] + i][self.current_position[1] + j] = 1
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        self.board = [row for row in self.board if any(cell == 0 for cell in row)]
        while len(self.board) < BOARD_HEIGHT:
            self.board.insert(0, [0] * BOARD_WIDTH)

@app.route('/api/game', methods=['POST'])
def start_game():
    game = Game()
    game.new_piece()
    return jsonify({'board': game.board, 'current_piece': game.current_piece, 'position': game.current_position})

@app.route('/api/game/move', methods=['POST'])
def move_game():
    data = request.json
    game = Game()
    game.move_piece(data['direction'])
    return jsonify({'board': game.board, 'current_piece': game.current_piece, 'position': game.current_position})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return jsonify({'message': 'File uploaded successfully'})

class TestGame(unittest.TestCase):
    def test_new_piece(self):
        game = Game()
        game.new_piece()
        self.assertIsNotNone(game.current_piece)

    def test_move_piece(self):
        game = Game()
        game.new_piece()
        initial_position = game.current_position
        game.move_piece('left')
        self.assertNotEqual(initial_position, game.current_position)

    def test_lock_piece(self):
        game = Game()
        game.new_piece()
        game.lock_piece()
        self.assertEqual(game.board[0][BOARD_WIDTH // 2 - len(game.current_piece[0]) // 2], 1)

if __name__ == '__main__':
    app.run(debug=False)