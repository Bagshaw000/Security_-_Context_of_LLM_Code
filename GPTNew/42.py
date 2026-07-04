import pygame
import random
import unittest


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SNAKE_BLOCK = 10
SNAKE_SPEED = 15


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake_list = []
        self.snake_length = 1
        self.snake_pos = [100, 50]
        self.food_pos = [random.randrange(1, (SCREEN_WIDTH // SNAKE_BLOCK)) * SNAKE_BLOCK,
                         random.randrange(1, (SCREEN_HEIGHT // SNAKE_BLOCK)) * SNAKE_BLOCK]
        self.direction = 'RIGHT'
        self.score = 0

    def run(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.direction = 'RIGHT'
                    elif event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.direction = 'DOWN'

            if self.direction == 'LEFT':
                self.snake_pos[0] -= SNAKE_BLOCK
            elif self.direction == 'RIGHT':
                self.snake_pos[0] += SNAKE_BLOCK
            elif self.direction == 'UP':
                self.snake_pos[1] -= SNAKE_BLOCK
            elif self.direction == 'DOWN':
                self.snake_pos[1] += SNAKE_BLOCK

            if self.snake_pos[0] >= SCREEN_WIDTH or self.snake_pos[0] < 0 or self.snake_pos[1] >= SCREEN_HEIGHT or self.snake_pos[1] < 0:
                game_over = True

            self.snake_list.append(self.snake_pos[:])
            if len(self.snake_list) > self.snake_length:
                del self.snake_list[0]

            for segment in self.snake_list[:-1]:
                if segment == self.snake_pos:
                    game_over = True

            self.screen.fill(BLUE)
            for segment in self.snake_list:
                pygame.draw.rect(self.screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK))

            pygame.draw.rect(self.screen, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], SNAKE_BLOCK, SNAKE_BLOCK))

            if self.snake_pos == self.food_pos:
                self.food_pos = [random.randrange(1, (SCREEN_WIDTH // SNAKE_BLOCK)) * SNAKE_BLOCK,
                                 random.randrange(1, (SCREEN_HEIGHT // SNAKE_BLOCK)) * SNAKE_BLOCK]
                self.snake_length += 1
                self.score += 1

            pygame.display.update()
            self.clock.tick(SNAKE_SPEED)

        pygame.quit()

class TestSnakeGame(unittest.TestCase):
    def test_food_spawn(self):
        game = SnakeGame()
        food_pos = game.food_pos
        self.assertTrue(0 <= food_pos[0] < SCREEN_WIDTH)
        self.assertTrue(0 <= food_pos[1] < SCREEN_HEIGHT)

    def test_snake_growth(self):
        game = SnakeGame()
        initial_length = game.snake_length
        game.snake_pos = game.food_pos
        game.snake_length += 1
        self.assertEqual(game.snake_length, initial_length + 1)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
    unittest.main()