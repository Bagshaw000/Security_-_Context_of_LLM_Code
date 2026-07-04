import curses
import random
import unittest
from collections import deque, namedtuple
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

Point = namedtuple('Point', ['x', 'y'])

class GameLogic:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        
        self.direction = Direction.RIGHT
        
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = deque([
            Point(start_x, start_y),
            Point(start_x - 1, start_y),
            Point(start_x - 2, start_y)
        ])
        self.score = 0
        self.food = None
        self._place_food()
        self.game_over = False

    def _place_food(self):
        
        while True:
            new_food = Point(
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if new_food not in self.snake:
                self.food = new_food
                break

    def change_direction(self, new_dir):
        
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def update(self):
        
        if self.game_over:
            return

        head = self.snake[0]
        dx, dy = 0, 0
        
        if self.direction == Direction.UP:
            dy = -1
        elif self.direction == Direction.DOWN:
            dy = 1
        elif self.direction == Direction.LEFT:
            dx = -1
        elif self.direction == Direction.RIGHT:
            dx = 1

        
        new_head = Point(
            (head.x + dx) % self.width,
            (head.y + dy) % self.height
        )

        
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.appendleft(new_head)

        
        if new_head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

class SnakeGameTerminal:
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._setup_curses()
        
        
        height, width = stdscr.getmaxyx()
        
        self.logic = GameLogic(width - 2, height - 2)
        
        self.key_map = {
            curses.KEY_UP: Direction.UP,
            curses.KEY_DOWN: Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
            curses.KEY_RIGHT: Direction.RIGHT,
            ord('w'): Direction.UP,
            ord('s'): Direction.DOWN,
            ord('a'): Direction.LEFT,
            ord('d'): Direction.RIGHT
        }

    def _setup_curses(self):
        curses.curs_set(0) 
        self.stdscr.nodelay(True) 
        self.stdscr.timeout(100) 
        self.stdscr.keypad(True) 

    def run(self):
        
        while not self.logic.game_over:
            self._draw()
            self._handle_input()
            self.logic.update()

        self._draw_game_over()

    def _handle_input(self):
        
        try:
            key = self.stdscr.getch()
            if key in self.key_map:
                self.logic.change_direction(self.key_map[key])
            elif key == ord('q'):
                self.logic.game_over = True
        except Exception:
            
            pass

    def _draw(self):
        self.stdscr.erase()
        
        
        try:
            self.stdscr.addch(self.logic.food.y, self.logic.food.x, '*')
            
            
            for i, p in enumerate(self.logic.snake):
                char = 'O' if i == 0 else 'o'
                self.stdscr.addch(p.y, p.x, char)
        except curses.error:
            
            pass

        self.stdscr.addstr(0, 0, f" Score: {self.logic.score} | Press 'q' to Quit ")
        self.stdscr.refresh()

    def _draw_game_over(self):
        self.stdscr.nodelay(False)
        msg = f" GAME OVER! Final Score: {self.logic.score}. Press any key. "
        h, w = self.stdscr.getmaxyx()
        try:
            self.stdscr.addstr(h // 2, (w - len(msg)) // 2, msg, curses.A_REVERSE)
            self.stdscr.refresh()
            self.stdscr.getch()
        except curses.error:
            pass



class TestSnakeGame(unittest.TestCase):
    
    def setUp(self):
        self.logic = GameLogic(width=20, height=20)

    def test_initial_state(self):
        self.assertEqual(len(self.logic.snake), 3)
        self.assertEqual(self.logic.score, 0)
        self.assertFalse(self.logic.game_over)

    def test_movement_and_wrapping(self):
        
        
        for _ in range(15):
            self.logic.update()
        
        head = self.logic.snake[0]
        
        self.assertEqual(head.x, 5)

    def test_score_increment(self):
        
        self.logic.food = Point(11, 10)
        self.logic.direction = Direction.RIGHT
        initial_len = len(self.logic.snake)
        
        self.logic.update()
        
        self.assertEqual(self.logic.score, 1)
        self.assertEqual(len(self.logic.snake), initial_len + 1)

    def test_collision_self(self):
        
        
        self.logic.snake = deque([Point(5, 5), Point(6, 5), Point(6, 6), Point(5, 6)])
        self.logic.direction = Direction.DOWN
        self.logic.update() 
        self.assertTrue(self.logic.game_over)

    def test_invalid_direction_change(self):
        
        self.logic.direction = Direction.RIGHT
        self.logic.change_direction(Direction.LEFT)
        self.assertEqual(self.logic.direction, Direction.RIGHT)

def run_tests():
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSnakeGame)
    unittest.TextTestRunner(verbosity=1).run(suite)

def main():
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
    else:
        try:
            curses.wrapper(lambda stdscr: SnakeGameTerminal(stdscr).run())
        except KeyboardInterrupt:
            pass 

if __name__ == "__main__":
    main()