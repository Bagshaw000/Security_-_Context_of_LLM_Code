import pygame
import sys
import random
from typing import List, Tuple, Optional


SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE


COLOR_BACKGROUND: Tuple[int, int, int] = (155, 188, 15)
COLOR_SNAKE: Tuple[int, int, int] = (15, 56, 15)
COLOR_FOOD: Tuple[int, int, int] = (48, 98, 48)


UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

class Snake:
    
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.length: int = 3
        self.positions: List[Tuple[int, int]] = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction: Tuple[int, int] = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score: int = 0
        self.alive: bool = True

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def turn(self, point: Tuple[int, int]) -> None:
        
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self) -> None:
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_pos: Tuple[int, int] = (cur_x + dir_x, cur_y + dir_y)

        
        if (new_pos[0] < 0 or new_pos[0] >= GRID_WIDTH or 
            new_pos[1] < 0 or new_pos[1] >= GRID_HEIGHT or 
            new_pos in self.positions[2:]):
            self.alive = False
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def grow(self) -> None:
        self.length += 1
        self.score += 1

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, COLOR_SNAKE, rect)
            
            pygame.draw.rect(surface, COLOR_BACKGROUND, rect, 1)

class Food:
    
    def __init__(self, snake_positions: List[Tuple[int, int]]) -> None:
        self.position: Tuple[int, int] = (0, 0)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: List[Tuple[int, int]]) -> None:
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def draw(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, COLOR_FOOD, rect)

class GameEngine:
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nokia Snake 1997 - Principal Engineer Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.snake = Snake()
        self.food = Food(self.snake.positions)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn(RIGHT)

    def update(self) -> None:
        if self.snake.alive:
            self.snake.move()
            if self.snake.get_head_position() == self.food.position:
                self.snake.grow()
                self.food.randomize_position(self.snake.positions)
        else:
            
            self.snake.reset()
            self.food.randomize_position(self.snake.positions)

    def render(self) -> None:
        self.screen.fill(COLOR_BACKGROUND)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        
        score_text = self.font.render(f"SCORE: {self.snake.score}", True, COLOR_SNAKE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def run(self) -> None:
        
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(12)

if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
