import curses
import random


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()


snake = [(screen_height//2, screen_width//2)]
food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
direction = curses.KEY_RIGHT


while True:
    
    screen.clear()

    
    for segment in snake:
        screen.addch(segment[0], segment[1], '

    
    screen.addch(food[0], food[1], '@')

    
    key = screen.getch()

    
    if key == curses.KEY_UP and direction != curses.KEY_DOWN:
        direction = curses.KEY_UP
    elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
        direction = curses.KEY_DOWN
    elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
        direction = curses.KEY_LEFT
    elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
        direction = curses.KEY_RIGHT

    
    new_head = (snake[0][0] + (direction == curses.KEY_UP and -1) + (direction == curses.KEY_DOWN and 1), snake[0][1] + (direction == curses.KEY_LEFT and -1) + (direction == curses.KEY_RIGHT and 1))

    
    if new_head in snake or new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1:
        break

    
    snake.insert(0, new_head)

    
    if new_head == food:
        food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
    else:
        snake.pop()

    
    screen.refresh()


curses.endwin()