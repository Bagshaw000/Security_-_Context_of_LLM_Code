import pygame
import time
import random


pygame.init()


COLOR_SCREEN = (139, 172, 15)  
COLOR_SNAKE = (15, 56, 15)     
COLOR_FOOD = (48, 98, 48)


WIDTH = 400
HEIGHT = 300
BLOCK_SIZE = 20


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Nokia Snake 1997')

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("arial", 20)

def display_score(score):
    value = font_style.render("Score: " + str(score), True, COLOR_SNAKE)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, COLOR_SNAKE, [x[0], x[1], block_size, block_size])

def game_loop():
    game_over = False
    game_close = False

    
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    
    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0

    while not game_over:

        while game_close:
            screen.fill(COLOR_SCREEN)
            msg = font_style.render("Game Over! Press C-Play or Q-Quit", True, COLOR_SNAKE)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(COLOR_SCREEN)
        
        pygame.draw.rect(screen, COLOR_FOOD, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            length_of_snake += 1

        clock.tick(10)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()