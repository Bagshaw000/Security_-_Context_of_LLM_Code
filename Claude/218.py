import curses
import random


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()


snake = [(screen_height//2, screen_width//2)]
direction = 'right'


food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))


while True:
    
    screen.clear()

    
    for segment in snake:
        screen.addch(segment[0], segment[1], '

    
    screen.addch(food[0], food[1], '@')

    
    key = screen.getch()

    
    if key == curses.KEY_UP and direction != 'down':
        direction = 'up'
    elif key == curses.KEY_DOWN and direction != 'up':
        direction = 'down'
    elif key == curses.KEY_LEFT and direction != 'right':
        direction = 'left'
    elif key == curses.KEY_RIGHT and direction != 'left':
        direction = 'right'

    
    new_head = list(snake[0])
    if direction == 'up':
        new_head[0] -= 1
    elif direction == 'down':
        new_head[0] += 1
    elif direction == 'left':
        new_head[1] -= 1
    elif direction == 'right':
        new_head[1] += 1

    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake:
        break

    
    snake.insert(0, tuple(new_head))

    
    if new_head == food:
        food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
    else:
        snake.pop()

    
    screen.refresh()


curses.endwin()