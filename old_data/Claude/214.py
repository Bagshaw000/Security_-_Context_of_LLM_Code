import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()
window = curses.newwin(screen_height, screen_width, 0, 0)
window.keypad(1)
window.timeout(100)


snake = [(screen_height//2, screen_width//2)]
snake_direction = KEY_RIGHT


food = (randint(1, screen_height-2), randint(1, screen_width-2))


while True:
    
    window.clear()

    
    for segment in snake:
        window.addch(segment[0], segment[1], '

    
    window.addch(food[0], food[1], '@')

    
    key = window.getch()
    if key == -1:
        snake_direction = snake_direction
    elif key == KEY_RIGHT:
        snake_direction = KEY_RIGHT
    elif key == KEY_LEFT:
        snake_direction = KEY_LEFT
    elif key == KEY_UP:
        snake_direction = KEY_UP
    elif key == KEY_DOWN:
        snake_direction = KEY_DOWN

    
    new_head = (snake[0][0], snake[0][1])
    if snake_direction == KEY_RIGHT:
        new_head = (new_head[0], new_head[1] + 1)
    elif snake_direction == KEY_LEFT:
        new_head = (new_head[0], new_head[1] - 1)
    elif snake_direction == KEY_UP:
        new_head = (new_head[0] - 1, new_head[1])
    elif snake_direction == KEY_DOWN:
        new_head = (new_head[0] + 1, new_head[1])

    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake:
        break

    snake.insert(0, new_head)
    if new_head == food:
        food = (randint(1, screen_height-2), randint(1, screen_width-2))
    else:
        snake.pop()


curses.endwin()