import pygame
import random
import sys
from enum import Enum
from collections import namedtuple


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20
FPS = 10


COLOR_BG = (143, 155, 11)    
COLOR_SNAKE = (30, 30, 30)   
COLOR_FOOD = (30, 30, 30)

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.w = width
        self.h = height
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake - Nokia 1997 Retro')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - CELL_SIZE, self.head.y),
            Point(self.head.x - (2 * CELL_SIZE), self.head.y)
        ]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (self.h - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        self.frame_iteration += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        
        self._move(self.direction)
        self.snake.insert(0, self.head)

        
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score

        
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        
        self._update_ui()
        self.clock.tick(FPS)
        return game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        
        if pt.x > self.w - CELL_SIZE or pt.x < 0 or pt.y > self.h - CELL_SIZE or pt.y < 0:
            return True
        
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(COLOR_BG)

        for pt in self.snake:
            pygame.draw.rect(self.display, COLOR_SNAKE, pygame.Rect(pt.x, pt.y, CELL_SIZE, CELL_SIZE))
            
            pygame.draw.rect(self.display, COLOR_BG, pygame.Rect(pt.x + 2, pt.y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 1)

        pygame.draw.rect(self.display, COLOR_FOOD, pygame.Rect(self.food.x, self.food.y, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += CELL_SIZE
        elif direction == Direction.LEFT:
            x -= CELL_SIZE
        elif direction == Direction.DOWN:
            y += CELL_SIZE
        elif direction == Direction.UP:
            y -= CELL_SIZE
        self.head = Point(x, y)

if __name__ == '__main__':
    pygame.init()
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()
        if game_over:
            break

    print(f'Final Score: {score}')
    pygame.quit()