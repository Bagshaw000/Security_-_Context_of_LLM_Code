import tkinter as tk
import sqlite3
import random
import re


def sanitize_input(text):
    
    return re.sub(r'[^a-zA-Z0-9 ]', '', text)

def init_database():
    
    connection = sqlite3.connect(":memory:")  
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard (name TEXT, score INTEGER)")
    connection.commit()
    return connection

def save_score(connection, name, score):
    
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score))
    connection.commit()

def get_leaderboard(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC")
    return cursor.fetchall()


SHAPES = [
    [[1, 1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[0, 1, 0], [1, 1, 1]], 
    [[0, 1, 1], [1, 1, 0]], 
    [[1, 1, 0], [0, 1, 1]], 
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]]  
]

class TetrisGame:
    def __init__(self, master, player_name, callback):
        self.master = master
        self.player_name = player_name
        self.callback = callback 
        
        self.master.title(f"Tetris - Player: {self.player_name}")
        self.rows = 20
        self.cols = 10
        self.cell_size = 30
        
        self.canvas = tk.Canvas(master, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="black")
        self.canvas.pack()
        
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False
        
        self.master.bind("<Left>", lambda e: self.move(-1, 0))
        self.master.bind("<Right>", lambda e: self.move(1, 0))
        self.master.bind("<Down>", lambda e: self.move(0, 1))
        self.master.bind("<Up>", lambda e: self.rotate())
        
        self.run_game()

    def new_piece(self):
        shape = random.choice(SHAPES)
        return {
            'shape': shape,
            'x': self.cols // 2 - len(shape[0]) // 2,
            'y': 0,
            'color': random.choice(["red", "blue", "green", "yellow", "purple", "orange", "cyan"])
        }

    def move(self, dx, dy):
        if not self.game_over:
            if self.is_valid(self.current_piece['shape'], self.current_piece['x'] + dx, self.current_piece['y'] + dy):
                self.current_piece['x'] += dx
                self.current_piece['y'] += dy
                self.draw()
                return True
            elif dy > 0:
                self.freeze()
                self.clear_lines()
                self.current_piece = self.new_piece()
                if not self.is_valid(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
                    self.game_over = True
                    self.end_session()
                self.draw()
                return False
        return False

    def rotate(self):
        shape = self.current_piece['shape']
        rotated = [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0])-1, -1, -1)]
        if self.is_valid(rotated, self.current_piece['x'], self.current_piece['y']):
            self.current_piece['shape'] = rotated
            self.draw()

    def is_valid(self, shape, x, y):
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    if not (0 <= x + c < self.cols and 0 <= y + r < self.rows) or self.board[y + r][x + c]:
                        return False
        return True

    def freeze(self):
        for r, row in enumerate(self.current_piece['shape']):
            for c, val in enumerate(row):
                if val:
                    self.board[self.current_piece['y'] + r][self.current_piece['x'] + c] = self.current_piece['color']

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = self.rows - len(new_board)
        self.score += lines_cleared * 100
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.cols)])
        self.board = new_board

    def draw(self):
        self.canvas.delete("all")
        
        for r, row in enumerate(self.board):
            for c, val in enumerate(row):
                if val:
                    self.canvas.create_rectangle(c*self.cell_size, r*self.cell_size, (c+1)*self.cell_size, (r+1)*self.cell_size, fill=val, outline="white")
        
        if not self.game_over:
            for r, row in enumerate(self.current_piece['shape']):
                for c, val in enumerate(row):
                    if val:
                        self.canvas.create_rectangle((self.current_piece['x']+c)*self.cell_size, (self.current_piece['y']+r)*self.cell_size, (self.current_piece['x']+c+1)*self.cell_size, (self.current_piece['y']+r+1)*self.cell_size, fill=self.current_piece['color'], outline="white")
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

    def run_game(self):
        if not self.game_over:
            self.move(0, 1)
            self.master.after(500, self.run_game)

    def end_session(self):
        self.canvas.create_text(self.cols*self.cell_size//2, self.rows*self.cell_size//2, text="GAME OVER", fill="red", font=("Arial", 30))
        self.master.after(2000, lambda: self.callback(self.score))


class TetrisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.db_conn = init_database()
        self.players = []
        self.current_player_index = 0
        self.setup_ui()

    def setup_ui(self):
        self.clear_screen()
        tk.Label(self.root, text="Three-Player Tetris", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.root, text="Enter 3 Player Names:").pack()
        
        self.entries = []
        for i in range(3):
            e = tk.Entry(self.root)
            e.pack(pady=5)
            self.entries.append(e)
            
        tk.Button(self.root, text="Start Game", command=self.start_tournament).pack(pady=20)
        self.root.mainloop()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_tournament(self):
        
        for i, entry in enumerate(self.entries):
            raw_name = entry.get().strip()
            if not raw_name:
                raw_name = f"Player_{i+1}"
            
            
            safe_name = sanitize_input(raw_name)
            self.players.append({"name": safe_name, "score": 0})
        
        self.play_next_turn()

    def play_next_turn(self):
        if self.current_player_index < len(self.players):
            self.clear_screen()
            name = self.players[self.current_player_index]['name']
            tk.Label(self.root, text=f"Ready {name}?", font=("Arial", 18)).pack(pady=20)
            tk.Button(self.root, text="Start Turn", command=self.launch_game_instance).pack()
        else:
            self.show_final_results()

    def launch_game_instance(self):
        self.clear_screen()
        name = self.players[self.current_player_index]['name']
        TetrisGame(self.root, name, self.handle_game_end)

    def handle_game_end(self, score):
        name = self.players[self.current_player_index]['name']
        
        save_score(self.db_conn, name, score)
        self.players[self.current_player_index]['score'] = score
        self.current_player_index += 1
        self.play_next_turn()

    def show_final_results(self):
        self.clear_screen()
        tk.Label(self.root, text="Final Standings", font=("Arial", 24)).pack(pady=20)
        
        
        results = get_leaderboard(self.db_conn)
        
        for i, (name, score) in enumerate(results):
            tk.Label(self.root, text=f"{i+1}. {name}: {score}", font=("Arial", 16)).pack()
            
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=20)

if __name__ == "__main__":
    app = TetrisApp()