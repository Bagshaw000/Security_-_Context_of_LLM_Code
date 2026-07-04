import random
import curses


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()
snake_body = [(screen_height//2, screen_width//2)]
food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
direction = (0, 1)

while True:
    screen.clear()
    screen.border(0)
    
    
    for segment in snake_body:
        screen.addch(segment[0], segment[1], '
    
    
    screen.addch(food[0], food[1], '@')
    
    
    key = screen.getch()
    
    
    if key == curses.KEY_UP:
        direction = (-1, 0)
    elif key == curses.KEY_DOWN:
        direction = (1, 0)
    elif key == curses.KEY_LEFT:
        direction = (0, -1)
    elif key == curses.KEY_RIGHT:
        direction = (0, 1)
    
    
    new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
    
    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake_body:
        break
    
    snake_body.insert(0, new_head)
    
    
    if new_head == food:
        food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
    else:
        snake_body.pop()
    
    screen.refresh()

curses.endwin()