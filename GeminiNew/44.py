import tkinter as tk
import random




SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GAME_SPEED = 100  
SPACE_SIZE = 20   
SNAKE_COLOR = "
FOOD_COLOR = "
BACKGROUND_COLOR = "

class SnakeGame:
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.title("Nokia Snake 1997 - Harold Edition")
        self.window.resizable(False, False)

        self.score = 0
        self.direction = 'down'

        
        self.label = tk.Label(self.window, text="Score: {}".format(self.score), font=('consolas', 40))
        self.label.pack()

        
        self.canvas = tk.Canvas(self.window, bg=BACKGROUND_COLOR, height=SCREEN_HEIGHT, width=SCREEN_WIDTH)
        self.canvas.pack()

        self.window.update()

        
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))

        
        self.snake_coordinates = [[0, 0], [0, 0], [0, 0]]
        self.snake_squares = []
        self.food_coordinates = [0, 0]

        
        self.create_snake()
        self.create_food()
        self.next_turn()

        self.window.mainloop()

    def create_snake(self):
        
        for x, y in self.snake_coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.snake_squares.append(square)

    def create_food(self):
        
        x = random.randint(0, int((SCREEN_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((SCREEN_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.food_coordinates = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

    def next_turn(self):
        
        x, y = self.snake_coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        
        self.snake_coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.snake_squares.insert(0, square)

        
        if x == self.food_coordinates[0] and y == self.food_coordinates[1]:
            self.score += 1
            self.label.config(text="Score: {}".format(self.score))
            self.canvas.delete("food")
            self.create_food()
        else:
            
            del self.snake_coordinates[-1]
            self.canvas.delete(self.snake_squares[-1])
            del self.snake_squares[-1]

        
        if self.check_collisions(x, y):
            self.game_over()
        else:
            self.window.after(GAME_SPEED, self.next_turn)

    def change_direction(self, new_direction):
        
        old_direction = self.direction

        if new_direction == 'left' and old_direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and old_direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and old_direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and old_direction != 'up':
            self.direction = new_direction

    def check_collisions(self, x, y):
        
        
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True

        
        for body_part in self.snake_coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2,
                                font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

if __name__ == "__main__":
    
    try:
        SnakeGame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")