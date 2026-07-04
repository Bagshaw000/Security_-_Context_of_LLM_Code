import pygame
import sys, time
import random

pygame.init()

display_width = 240
display_height = 160
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)

snake_pos = [150, 50]
direction = 'right'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'up'
            elif event.key == pygame.K_DOWN:
                direction = 'down'
            elif event.key == pygame.K_LEFT:
                direction = 'left'
            elif event.key == pygame.K_RIGHT:
                direction = 'right'

    if direction == 'right':
        snake_pos[0] += 10
    elif direction == 'left':
        snake_pos[0] -= 10
    elif direction == 'up':
        snake_pos[1] -= 10
    elif direction == 'down':
        snake_pos[1] += 10

    screen.fill((255, 255, 255))
    for pos in snake_pos:
        pygame.draw.rect(screen, (0, 0, 0), [pos, 20, 20, 20])
    pygame.display.update()

    if (snake_pos[0]%display_width == 0) or (snake_pos[1]%display_height == 0):
        print('Game over')
        sys.exit()
    elif (snake_pos in snake_pos[:-1]):
        print('Game over')
        sys.exit()

    clock.tick(10)