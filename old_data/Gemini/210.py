import pygame
import sys
import random



SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
FPS = 10


COLOR_LCD_GREEN = (155, 188, 15)
COLOR_SNAKE_DARK = (15, 56, 15)
COLOR_FOOD_DARK = (48, 98, 48)

class SnakeGame:
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Nokia Snake 1997 - Junior Dev Edition')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)
        self.reset()

    def reset(self):
        
        self.direction = 'RIGHT'
        self.head = [100, 60]
        
        self.snake_body = [[100, 60], [80, 60], [60, 60]]
        self.food_pos = self._place_food()
        self.score = 0
        self.game_over = False

    def _place_food(self):
        
        x = random.randrange(0, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
        y = random.randrange(0, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
        
        if [x, y] in self.snake_body:
            return self._place_food()
        return [x, y]

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
        
        if self.direction == 'UP':
            self.head[1] -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            self.head[1] += BLOCK_SIZE
        elif self.direction == 'LEFT':
            self.head[0] -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            self.head[0] += BLOCK_SIZE

        
        if (self.head[0] < 0 or self.head[0] >= SCREEN_WIDTH or 
            self.head[1] < 0 or self.head[1] >= SCREEN_HEIGHT):
            self.game_over = True
            return

        
        if self.head in self.snake_body[1:]:
            self.game_over = True
            return

        
        self.snake_body.insert(0, list(self.head))

        
        if self.head == self.food_pos:
            self.score += 1
            self.food_pos = self._place_food()
        else:
            
            self.snake_body.pop()

    def draw(self):
        self.display.fill(COLOR_LCD_GREEN)
        
        
        for pos in self.snake_body:
            pygame.draw.rect(self.display, COLOR_SNAKE_DARK, 
                             pygame.Rect(pos[0], pos[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        
        pygame.draw.rect(self.display, COLOR_FOOD_DARK, 
                         pygame.Rect(self.food_pos[0], self.food_pos[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_SNAKE_DARK)
        self.display.blit(score_text, [10, 10])
        
        pygame.display.flip()

    def run(self):
        
        while not self.game_over:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        print(f"Final Score: {self.score}")
        pygame.quit()

if __name__ == '__main__':
    
    game = SnakeGame()
    game.run()