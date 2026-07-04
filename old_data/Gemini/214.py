import pygame
import random
import sys


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
FPS = 10


COLOR_BACKGROUND = (139, 172, 15)
COLOR_SNAKE = (15, 56, 15)
COLOR_FOOD = (48, 98, 48)
COLOR_TEXT = (15, 56, 15)

class SnakeGameLogic:
    
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        
        self.snake = [
            (self.width // 2, self.height // 2),
            (self.width // 2 - self.grid_size, self.height // 2),
            (self.width // 2 - (2 * self.grid_size), self.height // 2)
        ]
        self.direction = pygame.K_RIGHT
        self.score = 0
        self.game_over = False
        self.food = self._generate_food()

    def _generate_food(self):
        while True:
            x = random.randint(0, (self.width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(0, (self.height - self.grid_size) // self.grid_size) * self.grid_size
            if (x, y) not in self.snake:
                return (x, y)

    def update(self, new_direction):
        if self.game_over:
            return

        
        opposing_dirs = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT
        }
        if new_direction in opposing_dirs and new_direction != opposing_dirs.get(self.direction):
            self.direction = new_direction

        
        head_x, head_y = self.snake[0]
        if self.direction == pygame.K_UP:
            head_y -= self.grid_size
        elif self.direction == pygame.K_DOWN:
            head_y += self.grid_size
        elif self.direction == pygame.K_LEFT:
            head_x -= self.grid_size
        elif self.direction == pygame.K_RIGHT:
            head_x += self.grid_size

        new_head = (head_x, head_y)

        
        if (head_x < 0 or head_x >= self.width or 
            head_y < 0 or head_y >= self.height):
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

def main():
    pygame.init()
    
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake 1997 - Nokia Edition")
    clock = pygame.time.Clock()
    
    
    try:
        font = pygame.font.SysFont("Courier", 18, bold=True)
        large_font = pygame.font.SysFont("Courier", 32, bold=True)
    except:
        font = pygame.font.Font(None, 24)
        large_font = pygame.font.Font(None, 48)

    game = SnakeGameLogic(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)
    current_direction = pygame.K_RIGHT

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    current_direction = event.key
                if game.game_over and event.key == pygame.K_r:
                    game.reset()
                    current_direction = pygame.K_RIGHT

        
        if not game.game_over:
            game.update(current_direction)

        
        screen.fill(COLOR_BACKGROUND)

        
        food_rect = pygame.Rect(game.food[0] + 2, game.food[1] + 2, GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.rect(screen, COLOR_FOOD, food_rect)

        
        for i, segment in enumerate(game.snake):
            
            seg_rect = pygame.Rect(segment[0] + 1, segment[1] + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(screen, COLOR_SNAKE, seg_rect)
            
        
        score_surface = font.render(f"SCORE: {game.score}", True, COLOR_TEXT)
        screen.blit(score_surface, (10, 10))

        
        if game.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((139, 172, 15, 180)) 
            screen.blit(overlay, (0,0))
            
            msg = large_font.render("GAME OVER", True, COLOR_TEXT)
            retry_msg = font.render("PRESS 'R' TO RESTART", True, COLOR_TEXT)
            
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            retry_rect = retry_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            
            screen.blit(msg, msg_rect)
            screen.blit(retry_msg, retry_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()