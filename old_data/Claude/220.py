import random
import curses


window = curses.initscr()
curses.curs_set(0)
window_height, window_width = window.getmaxyx()


GAME_HEIGHT = window_height - 2
GAME_WIDTH = window_width - 2


snake = [(GAME_HEIGHT // 2, GAME_WIDTH // 2)]
food = (random.randint(1, GAME_HEIGHT - 1), random.randint(1, GAME_WIDTH - 1))


direction = curses.KEY_RIGHT


while True:
    
    window.clear()

    
    for segment in snake:
        window.addch(segment[0], segment[1], '

    
    window.addch(food[0], food[1], '@')

    
    key = window.getch()
    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        direction = key

    
    new_head = (snake[0][0], snake[0][1])
    if direction == curses.KEY_UP:
        new_head = (new_head[0] - 1, new_head[1])
    elif direction == curses.KEY_DOWN:
        new_head = (new_head[0] + 1, new_head[1])
    elif direction == curses.KEY_LEFT:
        new_head = (new_head[0], new_head[1] - 1)
    elif direction == curses.KEY_RIGHT:
        new_head = (new_head[0], new_head[1] + 1)

    
    if new_head[0] < 1 or new_head[0] >= GAME_HEIGHT or new_head[1] < 1 or new_head[1] >= GAME_WIDTH or new_head in snake:
        break

    
    snake.insert(0, new_head)
    if new_head == food:
        food = (random.randint(1, GAME_HEIGHT - 1), random.randint(1, GAME_WIDTH - 1))
    else:
        snake.pop()

    
    window.refresh()


curses.endwin()