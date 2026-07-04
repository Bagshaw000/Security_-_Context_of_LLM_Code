import curses
import random
import sys

def validate_dimensions(height, width):
    
    min_h, min_w = 10, 20
    if height < min_h or width < min_w:
        return False
    return True

def get_safe_input(current_key, next_key):
    
    opposites = {
        curses.KEY_UP: curses.KEY_DOWN,
        curses.KEY_DOWN: curses.KEY_UP,
        curses.KEY_LEFT: curses.KEY_RIGHT,
        curses.KEY_RIGHT: curses.KEY_LEFT
    }
    
    if next_key in opposites.keys():
        if next_key != opposites.get(current_key):
            return next_key
    return current_key

def main(stdscr):
    
    try:
        curses.curs_set(0) 
        stdscr.nodelay(1)  
        stdscr.timeout(100) 
    except curses.error:
        return

    
    sh, sw = stdscr.getmaxyx()
    if not validate_dimensions(sh, sw):
        sys.exit("Terminal window too small for Snake.")

    
    
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    
    food = [sh // 2, sw // 2]
    try:
        stdscr.addch(food[0], food[1], curses.ACS_PI)
    except curses.error:
        pass

    current_direction = curses.KEY_RIGHT

    while True:
        
        user_input = stdscr.getch()
        current_direction = get_safe_input(current_direction, user_input)

        
        head_y, head_x = snake[0]
        if current_direction == curses.KEY_DOWN:
            head_y += 1
        elif current_direction == curses.KEY_UP:
            head_y -= 1
        elif current_direction == curses.KEY_LEFT:
            head_x -= 1
        elif current_direction == curses.KEY_RIGHT:
            head_x += 1

        new_head = [head_y, head_x]

        
        
        if (new_head[0] <= 0 or new_head[0] >= sh - 1 or
            new_head[1] <= 0 or new_head[1] >= sw - 1 or
            new_head in snake):
            break

        
        snake.insert(0, new_head)

        
        if snake[0] == food:
            food = None
            while food is None:
                
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
                food = nf if nf not in snake else None
            try:
                stdscr.addch(food[0], food[1], curses.ACS_PI)
            except curses.error:
                pass
        else:
            
            tail = snake.pop()
            try:
                stdscr.addch(tail[0], tail[1], ' ')
            except curses.error:
                pass

        
        try:
            stdscr.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
        except curses.error:
            
            break

        stdscr.refresh()

if __name__ == "__main__":
    
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        
        sys.exit(f"An unexpected error occurred: {e}")