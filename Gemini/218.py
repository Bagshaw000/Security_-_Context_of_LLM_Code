import pygame
import random
import sys
from enum import Enum
from collections import namedtuple




class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

Point = namedtuple('Point', 'x, y')


COLOR_LCD_GREEN = (143, 166, 48)
COLOR_LCD_DARK = (43, 58, 2)
BLOCK_SIZE = 20
INITIAL_SPEED = 10

class SnakeGame:
    
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        
        
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Nokia Snake 1997 - Legacy Edition')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)
        
        self.reset()

    def reset(self):
        
        self.direction = Direction.RIGHT
        self.head = Point(self.width / 2, self.height / 2)
        
        
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        
        self.frame_iteration += 1
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._shutdown()
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

        
        self._draw_ui()
        
        
        self.clock.tick(INITIAL_SPEED + (self.score // 2))
        
        return game_over, self.score

    def is_collision(self, pt=None):
        
        if pt is None:
            pt = self.head
        
        if pt.x > self.width - BLOCK_SIZE or pt.x < 0 or pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True
        
        if pt in self.snake[1:]:
            return True
        return False

    def _draw_ui(self):
        
        self.display.fill(COLOR_LCD_GREEN)

        
        for i, pt in enumerate(self.snake):
            
            pygame.draw.rect(self.display, COLOR_LCD_DARK, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            
            pygame.draw.rect(self.display, COLOR_LCD_GREEN, pygame.Rect(pt.x + 2, pt.y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1)

        
        pygame.draw.rect(self.display, COLOR_LCD_DARK, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        
        text = self.font.render(f"Score: {self.score}", True, COLOR_LCD_DARK)
        self.display.blit(text, [0, 0])
        
        pygame.display.flip()

    def _move(self, direction):
        
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

    def _shutdown(self):
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    
    game = SnakeGame()
    
    while True:
        is_game_over, final_score = game.play_step()
        
        if is_game_over:
            print(f"Session Terminated. Final Score: {final_score}")
            break
            
    pygame.quit()