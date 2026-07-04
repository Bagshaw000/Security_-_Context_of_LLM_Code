import pygame
import sys, os
import time

pygame.init()

width = 480
height = 240
win = pygame.display.set_mode((width,height))

pygame.display.set_caption("Snake Game")

font = pygame.font.Font(None,36)

clock = pygame.time.Clock()

sides = [(1,0), (0,1), (-1,0), (0,-1)]

class SnakeGame:
    def __init__(self):
        self.snake = [100, 200]
        self.dir = 'right'
        self.length = 2
        self.apple = []
        self.score = 0

    def draw_text(self, text, x,y,size=36):
        fnt = pygame.font.SysFont('arial', size)
        img = fnt.render(str(text), True, (255,255,255))
        win.blit(img, [x,y])

    def get_new_apple(self):
        while True:
            a = 100 + (time.time() % 2) * 50
            b = 200 + (time.time() % 3) * 70
            if not([a,b] in self.snake):
                return [a,b]

    def play(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.dir != 'right':
                        self.dir = 'left'
                    elif event.key == pygame.K_RIGHT and self.dir != 'left':
                        self.dir = 'right'
                    elif event.key == pygame.K_UP and self.dir != 'down':
                        self.dir = 'up'
                    elif event.key == pygame.K_DOWN and self.dir != 'up':
                        self.dir = 'down'

            head = self.snake[-1]
            if self.dir == 'left':
                new_head = [head[0] - 20, head[1]]
            elif self.dir == 'right':
                new_head = [head[0] + 20, head[1]]
            elif self.dir == 'up':
                new_head = [head[0], head[1] - 20]
            elif self.dir == 'down':
                new_head = [head[0], head[1] + 20]

            if not(new_head in self.snake[:-1]):
                self.length += 1
                self.apple = self.get_new_apple()
                self.snake.append(new_head)
                if self.apple == new_head:
                    self.score += 1
            else:
                run = False

            win.fill((0,0,0))
            for pos in self.snake:
                pygame.draw.rect(win,(255,255,255),(pos[0],pos[1],20,20))
            pygame.draw.rect(win,(0,255,0),(*self.apple,*[20]))
            self.draw_text(str(self.score), 10, 10)
            pygame.display.update()

            clock.tick(15)

        pygame.quit()
        sys.exit()

game = SnakeGame()
game.play()