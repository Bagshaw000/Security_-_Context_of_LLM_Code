class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (0, 1)  
        self.food = self.place_food()
        self.score = 0
        self.is_running = True

    def place_food(self):
        import random
        while True:
            food_position = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food_position not in self.snake:
                return food_position

    def change_direction(self, new_direction):
        opposite_directions = { (0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0) }
        if new_direction in opposite_directions and self.direction == opposite_directions[new_direction]:
            return  
        self.direction = new_direction

    def update(self):
        if not self.is_running:
            return

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.is_running = False  

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()  
        else:
            self.snake.pop()  

    def get_game_state(self):
        return {
            "snake": self.snake,
            "food": self.food,
            "score": self.score,
            "is_running": self.is_running
        }

    def reset_game(self):
        self.__init__()


if __name__ == "__main__":
    game = SnakeGame()
    while game.is_running:
        
        game.update()
        print(game.get_game_state())  
```