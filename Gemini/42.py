import pygame
import sys
import random



SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


COLOR_BG = (139, 172, 15)
COLOR_SNAKE = (15, 56, 15)
COLOR_FOOD = (15, 56, 15)

class SnakeGame:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nokia Snake 1997")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.direction = (1, 0)
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False

    def _generate_food(self):
        
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def handle_input(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.direction = (1, 0)

    def update(self):
        
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.game_over = True
            return

        
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        
        if new_head == self.food:
            self.score += 1
            self.food = self._generate_food()
        else:
            
            self.snake.pop()

    def render(self):
        
        self.screen.fill(COLOR_BG)

        
        for segment in self.snake:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, COLOR_SNAKE, rect)
            
            pygame.draw.rect(self.screen, COLOR_BG, rect, 1)

        
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, COLOR_FOOD, food_rect)
        
        inner_padding = 6
        inner_food = food_rect.inflate(-inner_padding, -inner_padding)
        pygame.draw.rect(self.screen, COLOR_BG, inner_food)

        pygame.display.flip()

    def run(self):
        
        while True:
            self.handle_input()
            if not self.game_over:
                self.update()
            else:
                
                pygame.time.delay(1000)
                self.reset_game()
            
            self.render()
            
            self.clock.tick(10)

if __name__ == "__main__":
    
    game = SnakeGame()
    game.run()