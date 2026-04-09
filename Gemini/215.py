import pygame
import sys
import random
from enum import Enum
from typing import List, Tuple, Optional

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

class NokiaSnakeGame:
    
    
    
    GRID_SIZE = 20
    CELL_SIZE = 20
    WIDTH = 400
    HEIGHT = 400
    
    
    COLOR_LCD_BG = (143, 155, 112)
    COLOR_PIXEL_DARK = (43, 51, 35)
    
    FPS = 10

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Nokia 1997 Snake - Principal Engineer Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.reset_game()

    def reset_game(self):
        
        start_x = self.GRID_SIZE // 2
        start_y = self.GRID_SIZE // 2
        
        
        self.snake: List[Point] = [
            Point(start_x, start_y),
            Point(start_x - 1, start_y),
            Point(start_x - 2, start_y)
        ]
        
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food: Optional[Point] = None
        self.score = 0
        self._place_food()
        self.game_over = False

    def _place_food(self):
        
        while True:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            new_food = Point(x, y)
            if new_food not in self.snake:
                self.food = new_food
                break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head = self.snake[0]
        dx, dy = self.direction.value
        
        
        new_head = Point(head.x + dx, head.y + dy)

        
        if (new_head.x < 0 or new_head.x >= self.GRID_SIZE or
            new_head.y < 0 or new_head.y >= self.GRID_SIZE):
            self.game_over = True
            return

        
        if new_head in self.snake:
            self.game_over = True
            return

        
        self.snake.insert(0, new_head)

        
        if new_head == self.food:
            self.score += 10
            self._place_food()
            
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(self.COLOR_LCD_BG)
        
        
        pygame.draw.rect(self.screen, self.COLOR_PIXEL_DARK, 
                         (0, 0, self.WIDTH, self.HEIGHT), 2)

        
        if self.food:
            food_rect = pygame.Rect(self.food.x * self.CELL_SIZE, 
                                   self.food.y * self.CELL_SIZE, 
                                   self.CELL_SIZE, self.CELL_SIZE)
            
            pygame.draw.rect(self.screen, self.COLOR_PIXEL_DARK, food_rect.inflate(-4, -4))

        
        for index, segment in enumerate(self.snake):
            segment_rect = pygame.Rect(segment.x * self.CELL_SIZE, 
                                      segment.y * self.CELL_SIZE, 
                                      self.CELL_SIZE, self.CELL_SIZE)
            
            pygame.draw.rect(self.screen, self.COLOR_PIXEL_DARK, segment_rect.inflate(-2, -2))
            
            
            if index == 0:
                eye_size = 4
                pygame.draw.rect(self.screen, self.COLOR_LCD_BG, 
                                 (segment_rect.centerx - 2, segment_rect.centery - 2, eye_size, eye_size))

        
        score_text = self.font.render(f"Score: {self.score}", True, self.COLOR_PIXEL_DARK)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((143, 155, 112, 200))
            self.screen.blit(overlay, (0, 0))
            
            msg = self.font.render("GAME OVER", True, self.COLOR_PIXEL_DARK)
            retry_msg = self.font.render("Press 'R' to Restart", True, self.COLOR_PIXEL_DARK)
            
            self.screen.blit(msg, (self.WIDTH // 2 - msg.get_width() // 2, self.HEIGHT // 2 - 20))
            self.screen.blit(retry_msg, (self.WIDTH // 2 - retry_msg.get_width() // 2, self.HEIGHT // 2 + 10))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = NokiaSnakeGame()
    game.run()