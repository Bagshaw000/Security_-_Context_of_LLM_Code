import random
import curses


screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()
snake_x = screen_width//2
snake_y = screen_height//2
snake = [(snake_x, snake_y)]
food_x = random.randint(1, screen_width-2)
food_y = random.randint(1, screen_height-2)
direction = "right"
score = 0

while True:
    screen.clear()
    screen.border(0)
    screen.addstr(food_y, food_x, "@")
    for x, y in snake:
        screen.addch(y, x, "
    screen.addstr(0, 0, f"Score: {score}")
    screen.refresh()

    key = screen.getch()
    if key == curses.KEY_LEFT and direction != "right":
        direction = "left"
    elif key == curses.KEY_RIGHT and direction != "left":
        direction = "right"
    elif key == curses.KEY_UP and direction != "down":
        direction = "up"
    elif key == curses.KEY_DOWN and direction != "up":
        direction = "down"
    elif key == ord('q'):
        break

    new_head_x, new_head_y = snake[0]
    if direction == "left":
        new_head_x -= 1
    elif direction == "right":
        new_head_x += 1
    elif direction == "up":
        new_head_y -= 1
    elif direction == "down":
        new_head_y += 1

    if new_head_x < 1 or new_head_x >= screen_width-1 or new_head_y < 1 or new_head_y >= screen_height-1 or (new_head_x, new_head_y) in snake:
        break

    snake.insert(0, (new_head_x, new_head_y))
    if new_head_x == food_x and new_head_y == food_y:
        score += 1
        food_x = random.randint(1, screen_width-2)
        food_y = random.randint(1, screen_height-2)
    else:
        snake.pop()

    curses.napms(100)

curses.endwin()