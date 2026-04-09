import pygame
import sys
import random


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FPS = 10


COLOR_BG = (155, 188, 15)      
COLOR_SNAKE = (15, 56, 15)     
COLOR_FOOD = (15, 56, 15)      

class SnakeGame:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nokia Snake 1997")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.reset_game()

    def reset_game(self):
        
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)  
        self.food = self._generate_food_position()
        self.score = 0
        self.is_game_over = False

    def _generate_food_position(self):
        
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in self.snake:
                return pos

    def handle_events(self):
        
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
        
        if self.is_game_over:
            return

        
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            self.is_game_over = True
            return

        
        if new_head in self.snake:
            self.is_game_over = True
            return

        
        self.snake.insert(0, new_head)

        
        if new_head == self.food:
            self.score += 1
            self.food = self._generate_food_position()
        else:
            
            self.snake.pop()

    def render(self):
        
        self.screen.fill(COLOR_BG)

        
        food_rect = pygame.Rect(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_FOOD, food_rect.inflate(-4, -4))

        
        for segment in self.snake:
            seg_rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            pygame.draw.rect(self.screen, COLOR_SNAKE, seg_rect.inflate(-2, -2))

        
        score_text = self.font.render(f"SCORE: {self.score}", True, COLOR_SNAKE)
        self.screen.blit(score_text, (10, 10))

        if self.is_game_over:
            over_text = self.font.render("GAME OVER", True, COLOR_SNAKE)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        
        while True:
            self.handle_events()
            self.update()
            self.render()
            
            if self.is_game_over:
                
                pygame.time.delay(1500)
                self.reset_game()
            
            self.clock.tick(FPS)

if __name__ == "__main__":
    
    
    game = SnakeGame()
    game.run()