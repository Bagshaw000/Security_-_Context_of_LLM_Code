import curses
from random import randint


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()


snake = [(screen_height//2, screen_width//2)]
snake_length = 1
snake_direction = curses.KEY_RIGHT


food = (randint(1, screen_height-2), randint(1, screen_width-2))


while True:
    
    screen.clear()

    
    for segment in snake:
        screen.addch(segment[0], segment[1], '

    
    screen.addch(food[0], food[1], '@')

    
    key = screen.getch()
    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        snake_direction = key

    
    new_head = (snake[0][0], snake[0][1])
    if snake_direction == curses.KEY_UP:
        new_head = (new_head[0]-1, new_head[1])
    elif snake_direction == curses.KEY_DOWN:
        new_head = (new_head[0]+1, new_head[1])
    elif snake_direction == curses.KEY_LEFT:
        new_head = (new_head[0], new_head[1]-1)
    elif snake_direction == curses.KEY_RIGHT:
        new_head = (new_head[0], new_head[1]+1)

    
    if new_head in snake or new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1:
        break

    
    snake.insert(0, new_head)

    
    if new_head == food:
        snake_length += 1
        food = (randint(1, screen_height-2), randint(1, screen_width-2))
    else:
        snake.pop()

    
    screen.refresh()


curses.endwin()