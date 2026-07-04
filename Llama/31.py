import random
import time

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class IShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'I'

class JShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'J'

class LShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'L'

class OShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'O'

class SShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'S'

class TShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'T'

class ZShape(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'Z'

class Grid:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def draw_shape(self, shape):
        if shape.type == 'I':
            for i in range(shape.y, self.height):
                self.grid[i][shape.x] = 1
        elif shape.type == 'J':
            self.grid[shape.y][shape.x] = 1
            for i in range(2, 3):
                self.grid[i][shape.x+1] = 1
                if i != 2:
                    self.grid[i][shape.x-1] = 1
        elif shape.type == 'L':
            self.grid[shape.y][shape.x] = 1
            for i in range(3, 4):
                self.grid[i][shape.x+1] = 1
                if i != 3:
                    self.grid[i][shape.x-1] = 1
        elif shape.type == 'O':
            self.grid[shape.y][shape.x] = 1
            for i in range(-1, 2):
                self.grid[shape.y+i][shape.x+i] = 1
        elif shape.type == 'S':
            self.grid[shape.y][shape.x] = 1
            if shape.x != 0:
                self.grid[shape.y+1][shape.x-1] = 1
            if shape.x < 2:
                self.grid[shape.y+1][shape.x+1] = 1
        elif shape.type == 'T':
            for i in range(3):
                self.grid[i][shape.x] = 1
        elif shape.type == 'Z':
            for i in range(shape.y, self.height-2):
                self.grid[i][shape.x] = 1

    def delete_rows(self):
        count = 0
        for i in range(self.height):
            if all(cell != 0 for cell in self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0]*self.width)
                count += 1
        return count

class Game:
    def __init__(self):
        self.grid = Grid()
        self.shapes = [IShape(4,0), JShape(3,0), LShape(2,0), OShape(0,0), SShape(0,0), TShape(0,0), ZShape(0,0)]
        self.score = 0
        self.speed = 100

    def update(self):
        for shape in self.shapes:
            self.grid.draw_shape(shape)
        if len(self.shapes) < 7:
            new_shape = random.choice(self.shapes)
            if new_shape.type == 'I':
                new_x = random.randint(4,5)
                new_y = 0
            elif new_shape.type == 'J' or new_shape.type == 'L':
                new_x = 2
                new_y = random.randint(1,5)
            else:
                new_x = 1
                new_y = random.randint(1,3)
            self.shapes.append(new_shape.copy())
            self.shapes[-1].x = new_x
            self.shapes[-1].y = new_y

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            screen.fill((0, 0, 0))
            self.update()
            self.delete_rows()
            pygame.display.flip()
            time.sleep(1/self.speed)

    def delete_rows(self):
        count = 0
        for i in range(self.grid.height):
            if all(cell != 0 for cell in self.grid.grid[i]):
                del self.grid.grid[i]
                self.grid.grid.insert(0, [0]*self.grid.width)
                count += 1
        return count