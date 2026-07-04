import collections
import enum
import random
import sys
import time
from dataclasses import dataclass
from typing import Deque, Set, Optional, Final

class Direction(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def get_opposite(cls, direction: 'Direction') -> 'Direction':
        opposites = {
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP,
            cls.LEFT: cls.RIGHT,
            cls.RIGHT: cls.LEFT
        }
        return opposites[direction]

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

class ScoreManager:
    
    MAX_SCORE: Final[int] = 2**31 - 1

    def __init__(self) -> None:
        self.__current_score: int = 0

    def increment(self, points: int) -> None:
        if points < 0:
            raise ValueError("Point increment must be non-negative.")
        
        if self.__current_score > self.MAX_SCORE - points:
            self.__current_score = self.MAX_SCORE
        else:
            self.__current_score += points

    @property
    def current_score(self) -> int:
        return self.__current_score

class Snake:
    
    def __init__(self, start_pos: Coordinate, initial_length: int = 3):
        self.__body: Deque[Coordinate] = collections.deque([start_pos])
        self.__body_set: Set[Coordinate] = {start_pos}
        self.__direction: Direction = Direction.RIGHT
        
        
        for i in range(1, initial_length):
            pos = Coordinate(start_pos.x - i, start_pos.y)
            self.__body.append(pos)
            self.__body_set.add(pos)

    @property
    def head(self) -> Coordinate:
        return self.__body[0]

    @property
    def body(self) -> Deque[Coordinate]:
        
        return self.__body.copy()

    def get_direction(self) -> Direction:
        return self.__direction

    def update_direction(self, new_direction: Direction) -> None:
        
        if new_direction != Direction.get_opposite(self.__direction):
            self.__direction = new_direction

    def move(self, grow: bool = False) -> Coordinate:
        new_head = Coordinate(
            self.head.x + self.__direction.value[0],
            self.head.y + self.__direction.value[1]
        )
        
        self.__body.appendleft(new_head)
        self.__body_set.add(new_head)
        
        if not grow:
            tail = self.__body.pop()
            self.__body_set.discard(tail)
            
        return new_head

    def contains_coordinate(self, coord: Coordinate) -> bool:
        
        return coord in self.__body_set

class GameState:
    
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__snake = Snake(Coordinate(width // 2, height // 2))
        self.__food: Optional[Coordinate] = None
        self.__score_manager = ScoreManager()
        self.__is_game_over = False
        self._spawn_food()

    def _spawn_food(self) -> None:
        
        while True:
            new_food = Coordinate(
                random.randint(0, self.__width - 1),
                random.randint(0, self.__height - 1)
            )
            if not self.__snake.contains_coordinate(new_food):
                self.__food = new_food
                break

    def step(self) -> bool:
        if self.__is_game_over:
            return False

        head = self.__snake.head
        next_x = head.x + self.__snake.get_direction().value[0]
        next_y = head.y + self.__snake.get_direction().value[1]
        next_coord = Coordinate(next_x, next_y)

        
        if not (0 <= next_x < self.__width and 0 <= next_y < self.__height):
            self.__is_game_over = True
            return False

        
        if self.__snake.contains_coordinate(next_coord):
            self.__is_game_over = True
            return False

        
        if next_coord == self.__food:
            self.__snake.move(grow=True)
            self.__score_manager.increment(10)
            self._spawn_food()
        else:
            self.__snake.move(grow=False)

        return True

    def get_render_data(self):
        return {
            "snake": self.__snake.body,
            "food": self.__food,
            "score": self.__score_manager.current_score,
            "game_over": self.__is_game_over,
            "dimensions": (self.__width, self.__height)
        }

    def input_direction(self, direction: Direction) -> None:
        self.__snake.update_direction(direction)

class GameEngine:
    
    def __init__(self, width: int = 20, height: int = 10):
        self.__state = GameState(width, height)
        self.__tick_rate = 0.15 

    def _render(self, data: dict) -> None:
        
        width, height = data["dimensions"]
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        f = data["food"]
        if f:
            grid[f.y][f.x] = "*"
            
        for i, segment in enumerate(data["snake"]):
            char = "O" if i == 0 else "o"
            if 0 <= segment.y < height and 0 <= segment.x < width:
                grid[segment.y][segment.x] = char

        output = f"Score: {data['score']}\n"
        output += "+" + "-" * width + "+\n"
        for row in grid:
            output += "|" + "".join(row) + "|\n"
        output += "+" + "-" * width + "+\n"
        
        sys.stdout.write("\033[H") 
        sys.stdout.write(output)
        sys.stdout.flush()

    def run(self) -> None:
        
        sys.stdout.write("\033[2J")
        
        try:
            while not self.__state.get_render_data()["game_over"]:
                
                
                self.__state.step()
                self._render(self.__state.get_render_data())
                time.sleep(self.__tick_rate)
            
            print("GAME OVER")
        except KeyboardInterrupt:
            print("\nSession Terminated.")

if __name__ == "__main__":
    
    
    engine = GameEngine(width=30, height=15)
    engine.run()