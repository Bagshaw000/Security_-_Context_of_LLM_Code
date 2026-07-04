import pygame
import sys
import random
from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass



SCREEN_WIDTH = 840
SCREEN_HEIGHT = 480
GRID_SIZE = 20
SNAKE_SPEED = 12


COLOR_BG = (155, 188, 15)      
COLOR_ELEMENT = (15, 56, 15)    
COLOR_BORDER = (139, 172, 15)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class SnakeGame:
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Nokia Snake 1997 - Principal Engineer Edition')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)
        self.reset()

    def reset(self):
        
        self.direction = Direction.RIGHT
        self.head = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        
        self.snake = [
            self.head,
            Point(self.head.x - GRID_SIZE, self.head.y),
            Point(self.head.x - (2 * GRID_SIZE), self.head.y)
        ]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
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
        if self.is_collision():
            game_over = True
            return game_over, self.score
            
        
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        
        self._update_ui()
        self.clock.tick(SNAKE_SPEED)
        return game_over, self.score

    def is_collision(self, pt: Optional[Point] = None) -> bool:
        
        if pt is None:
            pt = self.head
        
        if pt.x > SCREEN_WIDTH - GRID_SIZE or pt.x < 0 or pt.y > SCREEN_HEIGHT - GRID_SIZE or pt.y < 0:
            return True
        
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        
        self.display.fill(COLOR_BG)
        
        
        for i, pt in enumerate(self.snake):
            
            pygame.draw.rect(self.display, COLOR_ELEMENT, pygame.Rect(pt.x, pt.y, GRID_SIZE, GRID_SIZE))
            
            pygame.draw.rect(self.display, COLOR_BG, pygame.Rect(pt.x + 2, pt.y + 2, GRID_SIZE - 4, GRID_SIZE - 4), 1)

        
        pygame.draw.rect(self.display, COLOR_ELEMENT, pygame.Rect(self.food.x, self.food.y, GRID_SIZE, GRID_SIZE))
        
        
        text = self.font.render(f"Score: {self.score}", True, COLOR_ELEMENT)
        self.display.blit(text, [0, 0])
        
        pygame.display.flip()

    def _move(self, direction: Direction):
        
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += GRID_SIZE
        elif direction == Direction.LEFT:
            x -= GRID_SIZE
        elif direction == Direction.DOWN:
            y += GRID_SIZE
        elif direction == Direction.UP:
            y -= GRID_SIZE
            
        self.head = Point(x, y)

def main():
    
    game = SnakeGame()
    
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break
            
    print(f'Final Score: {score}')
    pygame.quit()

if __name__ == '__main__':
    main()