import pygame
import random
import sys
from enum import Enum
from collections import namedtuple
from typing import List, Tuple


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
SPEED = 12


COLOR_BG = (143, 166, 28)
COLOR_SNAKE = (15, 15, 15)
COLOR_FOOD = (15, 15, 15)

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        self.w = width
        self.h = height
        
        
        pygame.init()
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Nokia Snake 1997 - Legacy Edition')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)
        
        self.reset()

    def reset(self) -> None:
        
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        
        
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self) -> None:
        
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self) -> Tuple[bool, int]:
        
        
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
        if self._is_collision():
            game_over = True
            return game_over, self.score

        
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        
        self._update_ui()
        self.clock.tick(SPEED)
        
        return game_over, self.score

    def _is_collision(self, pt: Point = None) -> bool:
        
        if pt is None:
            pt = self.head
        
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self) -> None:
        
        self.display.fill(COLOR_BG)
        
        
        for pt in self.snake:
            
            pygame.draw.rect(self.display, COLOR_SNAKE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            
            pygame.draw.rect(self.display, COLOR_BG, pygame.Rect(pt.x + 2, pt.y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1)
            
        
        pygame.draw.rect(self.display, COLOR_FOOD, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_SNAKE)
        self.display.blit(score_text, [10, 10])
        
        pygame.display.flip()

    def _move(self, direction: Direction) -> None:
        
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()
    
    
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break
            
    print(f'Final Score: {score}')
    pygame.quit()