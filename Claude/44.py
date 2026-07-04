import random
import curses


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()
game_window = curses.newwin(screen_height, screen_width, 0, 0)
game_window.keypad(1)


snake = [(screen_height//2, screen_width//2)]
food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
score = 0


while True:
    
    key = game_window.getch()
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

    
    if new_head[0] < 1 or new_head[0] >= screen_height-1 or new_head[1] < 1 or new_head[1] >= screen_width-1 or new_head in snake:
        break

    
    snake.insert(0, new_head)
    if new_head == food:
        food = (random.randint(1, screen_height-2), random.randint(1, screen_width-2))
        score += 1
    else:
        snake.pop()

    
    game_window.clear()
    game_window.border(0)
    for segment in snake:
        game_window.addch(segment[0], segment[1], '
    game_window.addch(food[0], food[1], '@')
    game_window.addstr(0, 0, f"Score: {score}")
    game_window.refresh()


curses.endwin()
print(f"Game over! Your final score is {score}.")