import curses
import random


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()


snake = [(screen_height//2, screen_width//2)]
food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))


while True:
    
    screen.clear()

    
    for segment in snake:
        screen.addch(segment[0], segment[1], '

    
    screen.addch(food[0], food[1], '@')

    
    key = screen.getch()
    if key == curses.KEY_UP:
        new_head = (snake[0][0]-1, snake[0][1])
    elif key == curses.KEY_DOWN:
        new_head = (snake[0][0]+1, snake[0][1])
    elif key == curses.KEY_LEFT:
        new_head = (snake[0][0], snake[0][1]-1)
    elif key == curses.KEY_RIGHT:
        new_head = (snake[0][0], snake[0][1]+1)
    else:
        continue

    
    snake.insert(0, new_head)
    if new_head == food:
        food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
    else:
        snake.pop()

    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake[1:]:
        break

    
    screen.refresh()


curses.endwin()