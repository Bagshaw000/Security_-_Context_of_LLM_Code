import random
import curses


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

    
    new_head = (snake[-1][0] + random.choice([-1, 0, 1]), snake[-1][1] + random.choice([-1, 0, 1]))

    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake:
        break

    
    snake.append(new_head)

    
    if new_head == food:
        food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
    else:
        snake.pop(0)

    
    screen.refresh()


curses.endwin()