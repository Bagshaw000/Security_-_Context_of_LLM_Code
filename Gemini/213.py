import pygame
import random
import sys


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
FPS = 10


COLOR_SCREEN = (155, 188, 15)
COLOR_SNAKE = (15, 56, 15)
COLOR_FOOD = (15, 56, 15)

class SnakeGame:
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Nokia Snake 1997')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Courier', 20, bold=True)
        self.reset_game()

    def reset_game(self):
        self.direction = 'RIGHT'
        self.head = [100, 100]
        
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.food = self._generate_food_position()
        self.score = 0
        self.game_over = False

    def _generate_food_position(self):
        while True:
            x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            food_pos = [x, y]
            if food_pos not in self.snake:
                return food_pos

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'

    def update(self):
        
        new_x, new_y = self.head[0], self.head[1]
        if self.direction == 'UP':
            new_y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            new_y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            new_x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            new_x += BLOCK_SIZE

        self.head = [new_x, new_y]

        
        if (self.head[0] < 0 or self.head[0] >= SCREEN_WIDTH or
            self.head[1] < 0 or self.head[1] >= SCREEN_HEIGHT or
            self.head in self.snake):
            self.game_over = True
            return

        
        self.snake.insert(0, list(self.head))

        
        if self.head == self.food:
            self.score += 1
            self.food = self._generate_food_position()
        else:
            
            self.snake.pop()

    def draw(self):
        self.display.fill(COLOR_SCREEN)

        
        for segment in self.snake:
            pygame.draw.rect(self.display, COLOR_SNAKE, 
                             pygame.Rect(segment[0], segment[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        
        pygame.draw.rect(self.display, COLOR_FOOD, 
                         pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))

        
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_SNAKE)
        self.display.blit(score_text, [10, 10])

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        self.show_game_over()

    def show_game_over(self):
        self.display.fill(COLOR_SCREEN)
        msg = self.font.render("GAME OVER", True, COLOR_SNAKE)
        retry_msg = self.font.render("Press R to Restart", True, COLOR_SNAKE)
        self.display.blit(msg, [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 20])
        self.display.blit(retry_msg, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 10])
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.run()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()