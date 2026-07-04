import collections
import random

class GameConfig:
    
    WIDTH = 20
    HEIGHT = 10
    MAX_SCORE = 9999
    
    VALID_DIRECTIONS = frozenset(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    DIRECTION_VECTORS = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

class SnakeGame:
    
    def __init__(self):
        
        self.snake = collections.deque([(5, 5), (4, 5), (3, 5)])
        self.direction = 'RIGHT'
        self.food = (10, 5)
        self.score = 0
        self.game_over = False

    def _validate_direction_change(self, new_dir):
        
        if new_dir not in GameConfig.VALID_DIRECTIONS:
            return False
        
        dx, dy = GameConfig.DIRECTION_VECTORS[new_dir]
        cx, cy = GameConfig.DIRECTION_VECTORS[self.direction]
        
        
        return not (dx + cx == 0 and dy + cy == 0)

    def input_handler(self, raw_command):
        
        if not isinstance(raw_command, str):
            return

        
        sanitized = raw_command.strip().upper()
        if self._validate_direction_change(sanitized):
            self.direction = sanitized

    def step(self):
        
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = GameConfig.DIRECTION_VECTORS[self.direction]
        
        
        new_head = (head_x + dx, head_y + dy)

        
        if not (0 <= new_head[0] < GameConfig.WIDTH and 0 <= new_head[1] < GameConfig.HEIGHT):
            self.game_over = True
            return

        
        if new_head in self.snake:
            self.game_over = True
            return

        
        self.snake.appendleft(new_head)

        
        if new_head == self.food:
            self.score = min(self.score + 1, GameConfig.MAX_SCORE)
            self.food = self._spawn_food()
        else:
            
            self.snake.pop()

    def _spawn_food(self):
        
        while True:
            pos = (random.randint(0, GameConfig.WIDTH - 1), 
                   random.randint(0, GameConfig.HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def render_state(self):
        
        return {
            "snake": list(self.snake),
            "food": self.food,
            "score": self.score,
            "is_active": not self.game_over
        }

if __name__ == "__main__":
    
    engine = SnakeGame()
    
    engine.input_handler("UP")
    engine.step()
    state = engine.render_state()
    
    print(f"Score: {state['score']} | Status: {'Active' if state['is_active'] else 'Game Over'}")