import random

class Tetromino:
    shapes = [
        [(0,0), (1,0), (2,0), (3,0)],  
        [(0,0), (1,0), (1,1), (2,1)],  
        [(0,1), (1,0), (1,1), (2,0)],  
        [(0,0), (0,1), (1,0), (1,1)],  
        [(0,0), (1,0), (2,0), (1,1)],  
        [(0,1), (1,0), (1,1), (1,2)],  
        [(0,0), (0,1), (1,1), (2,1)]   
    ]

    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.x = 3
        self.y = 0

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for x in range(width)] for y in range(height)]
        self.players = [Tetromino() for _ in range(3)]

    def update(self):
        for player in self.players:
            for x, y in player.shape:
                if player.x + x < 0 or player.x + x >= self.width or player.y + y >= self.height or self.grid[player.y + y][player.x + x] != 0:
                    return False
            for x, y in player.shape:
                self.grid[player.y + y][player.x + x] = player.color
            player.y += 1
        return True

    def draw(self):
        for row in self.grid:
            print(row)

board = Board(10, 20)
while True:
    if not board.update():
        break
    board.draw()