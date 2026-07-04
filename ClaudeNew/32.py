import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE]

TETRIS_SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

class TetrisGame:
    def __init__(self, x_offset, player_name):
        self.x_offset = x_offset
        self.player_name = player_name
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.create_new_piece()
        self.piece_x = GRID_WIDTH // 2 - 1
        self.piece_y = 0
        self.score = 0
        self.game_over = False

    def create_new_piece(self):
        shape = random.choice(TETRIS_SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color}

    def can_place_piece(self, piece, x, y):
        for row_idx, row in enumerate(piece["shape"]):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = x + col_idx
                    grid_y = y + row_idx
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return False
                    if grid_y >= 0 and self.grid[grid_y][grid_x] != 0:
                        return False
        return True

    def place_piece(self, piece, x, y):
        for row_idx, row in enumerate(piece["shape"]):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = x + col_idx
                    grid_y = y + row_idx
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = piece["color"]

    def remove_full_rows(self):
        rows_to_remove = []
        for row_idx, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                rows_to_remove.append(row_idx)
        
        for row_idx in sorted(rows_to_remove, reverse=True):
            del self.grid[row_idx]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.score += 100

    def move_piece_down(self):
        if self.can_place_piece(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            self.place_piece(self.current_piece, self.piece_x, self.piece_y)
            self.remove_full_rows()
            self.current_piece = self.create_new_piece()
            self.piece_x = GRID_WIDTH // 2 - 1
            self.piece_y = 0
            if not self.can_place_piece(self.current_piece, self.piece_x, self.piece_y):
                self.game_over = True

    def move_piece_left(self):
        if self.can_place_piece(self.current_piece, self.piece_x - 1, self.piece_y):
            self.piece_x -= 1

    def move_piece_right(self):
        if self.can_place_piece(self.current_piece, self.piece_x + 1, self.piece_y):
            self.piece_x += 1

    def rotate_piece(self):
        original_shape = self.current_piece["shape"]
        self.current_piece["shape"] = [list(row) for row in zip(*reversed(self.current_piece["shape"]))]
        
        if not self.can_place_piece(self.current_piece, self.piece_x, self.piece_y):
            self.current_piece["shape"] = original_shape

    def draw(self, screen):
        start_x = self.x_offset
        start_y = 50
        
        pygame.draw.rect(screen, WHITE, (start_x, start_y, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)
        
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(
                        screen,
                        cell,
                        (start_x + col_idx * CELL_SIZE, start_y + row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        
        for row_idx, row in enumerate(self.current_piece["shape"]):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.current_piece["color"],
                        (start_x + (self.piece_x + col_idx) * CELL_SIZE, 
                         start_y + (self.piece_y + row_idx) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )

class ThreePlayerTetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Three-Player Tetris Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.players = [
            TetrisGame(50, "Player 1"),
            TetrisGame(350, "Player 2"),
            TetrisGame(650, "Player 3")
        ]
        
        self.fall_speed = 0
        self.fall_speed_threshold = 30

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not self.players[0].game_over:
                        self.players[0].move_piece_left()
                elif event.key == pygame.K_RIGHT:
                    if not self.players[0].game_over:
                        self.players[0].move_piece_right()
                elif event.key == pygame.K_DOWN:
                    if not self.players[0].game_over:
                        self.players[0].move_piece_down()
                elif event.key == pygame.K_UP:
                    if not self.players[0].game_over:
                        self.players[0].rotate_piece()
                
                elif event.key == pygame.K_a:
                    if not self.players[1].game_over:
                        self.players[1].move_piece_left()
                elif event.key == pygame.K_d:
                    if not self.players[1].game_over:
                        self.players[1].move_piece_right()
                elif event.key == pygame.K_s:
                    if not self.players[1].game_over:
                        self.players[1].move_piece_down()
                elif event.key == pygame.K_w:
                    if not self.players[1].game_over:
                        self.players[1].rotate_piece()
                
                elif event.key == pygame.K_j:
                    if not self.players[2].game_over:
                        self.players[2].move_piece_left()
                elif event.key == pygame.K_l:
                    if not self.players[2].game_over:
                        self.players[2].move_piece_right()
                elif event.key == pygame.K_k:
                    if not self.players[2].game_over:
                        self.players[2].move_piece_down()
                elif event.key == pygame.K_i:
                    if not self.players[2].game_over:
                        self.players[2].rotate_piece()
                
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True

    def update(self):
        self.fall_speed += 1
        if self.fall_speed >= self.fall_speed_threshold:
            for player in self.players:
                if not player.game_over:
                    player.move_piece_down()
            self.fall_speed = 0

    def draw(self):
        self.screen.fill(BLACK)
        
        title_text = self.font.render("THREE-PLAYER TETRIS", True, WHITE)
        self.screen.blit(title_text, (250, 10))
        
        for player in self.players:
            player_text = self.font.render(f"{player.player_name}: {player.score}", True, WHITE)
            self.screen.blit(player_text, (player.x_offset, 25))
            
            player.draw(self.screen)
            
            if player.game_over:
                game_over_text = self.font.render("GAME OVER", True, RED)
                self.screen.blit(game_over_text, (player.x_offset + 20, 250))
        
        instructions_text = self.font.render(
            "Player 1: Arrow Keys | Player 2: WASD | Player 3: IJKL | ESC to quit",
            True, WHITE
        )
        self.screen.blit(instructions_text, (50, 550))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ThreePlayerTetris()
    game.run()