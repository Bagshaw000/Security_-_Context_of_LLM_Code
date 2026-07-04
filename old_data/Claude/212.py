import curses
from random import randint


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()


snake = [(screen_height//2, screen_width//2)]
food = (randint(1, screen_height-2), randint(1, screen_width-2))
direction = 'right'
score = 0

while True:
    
    screen.clear()

    
    for segment in snake:
        screen.addch(segment[0], segment[1], '

    
    screen.addch(food[0], food[1], '@')

    
    new_head = (snake[-1][0], snake[-1][1])
    if direction == 'up':
        new_head = (new_head[0]-1, new_head[1])
    elif direction == 'down':
        new_head = (new_head[0]+1, new_head[1])
    elif direction == 'left':
        new_head = (new_head[0], new_head[1]-1)
    elif direction == 'right':
        new_head = (new_head[0], new_head[1]+1)

    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake:
        break

    snake.append(new_head)
    if new_head == food:
        food = (randint(1, screen_height-2), randint(1, screen_width-2))
        score += 1
    else:
        snake.pop(0)

    
    screen.refresh()
    screen.timeout(100)
    key = screen.getch()
    if key == curses.KEY_UP and direction != 'down':
        direction = 'up'
    elif key == curses.KEY_DOWN and direction != 'up':
        direction = 'down'
    elif key == curses.KEY_LEFT and direction != 'right':
        direction = 'left'
    elif key == curses.KEY_RIGHT and direction != 'left':
        direction = 'right'


curses.endwin()
print(f'Your score: {score}')