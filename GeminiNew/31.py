import asyncio
import json
import hmac
import hashlib
import time
import secrets
import enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict


BOARD_WIDTH = 10
BOARD_HEIGHT = 20
MAX_PLAYERS = 3
TICK_RATE = 0.5  
SECRET_KEY = b"production_shared_secret_for_hmac_verification"


SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

class Command(enum.Enum):
    MOVE_LEFT = "LEFT"
    MOVE_RIGHT = "RIGHT"
    ROTATE = "ROTATE"
    SOFT_DROP = "DROP"
    HARD_DROP = "HARD_DROP"
    JOIN = "JOIN"



class SecurityProvider:
    
    
    @staticmethod
    def sign_payload(payload: dict) -> str:
        message = json.dumps(payload, sort_keys=True).encode()
        return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

    @staticmethod
    def verify_payload(payload: dict, signature: str) -> bool:
        if not signature:
            return False
        expected = SecurityProvider.sign_payload(payload)
        return hmac.compare_digest(expected, signature)



class TetrisPiece:
    def __init__(self, shape_key: str):
        self.shape = SHAPES[shape_key]
        self.color = shape_key
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisBoard:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.active_piece: Optional[TetrisPiece] = None
        self.spawn_piece()

    def spawn_piece(self):
        shape_key = secrets.choice(list(SHAPES.keys()))
        self.active_piece = TetrisPiece(shape_key)
        if self.check_collision(self.active_piece.x, self.active_piece.y):
            self.game_over = True

    def check_collision(self, nx: int, ny: int, shape: List[List[int]] = None) -> bool:
        shape = shape or self.active_piece.shape
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    target_x, target_y = nx + c, ny + r
                    if not (0 <= target_x < BOARD_WIDTH and 0 <= target_y < BOARD_HEIGHT):
                        return True
                    if self.grid[target_y][target_x]:
                        return True
        return False

    def lock_piece(self):
        for r, row in enumerate(self.active_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    self.grid[self.active_piece.y + r][self.active_piece.x + c] = self.active_piece.color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(BOARD_WIDTH)])
        self.grid = new_grid
        self.score += (lines_cleared ** 2) * 100

    def move(self, dx: int, dy: int):
        if self.game_over: return
        if not self.check_collision(self.active_piece.x + dx, self.active_piece.y + dy):
            self.active_piece.x += dx
            self.active_piece.y += dy
            return True
        elif dy > 0:
            self.lock_piece()
            return False
        return False

    def rotate(self):
        if self.game_over: return
        original_shape = self.active_piece.shape
        self.active_piece.rotate()
        if self.check_collision(self.active_piece.x, self.active_piece.y):
            self.active_piece.shape = original_shape

    def get_state(self) -> dict:
        return {
            "grid": self.grid,
            "score": self.score,
            "game_over": self.game_over,
            "piece": {
                "x": self.active_piece.x,
                "y": self.active_piece.y,
                "shape": self.active_piece.shape
            } if self.active_piece else None
        }



class GameSession:
    
    def __init__(self):
        self.players: Dict[str, TetrisBoard] = {}
        self.start_time = None
        self.is_active = False

    def add_player(self, player_id: str) -> bool:
        if len(self.players) < MAX_PLAYERS:
            self.players[player_id] = TetrisBoard()
            return True
        return False

    def process_input(self, player_id: str, command: str):
        if not self.is_active or player_id not in self.players:
            return
        
        board = self.players[player_id]
        if command == Command.MOVE_LEFT.value:
            board.move(-1, 0)
        elif command == Command.MOVE_RIGHT.value:
            board.move(1, 0)
        elif command == Command.ROTATE.value:
            board.rotate()
        elif command == Command.SOFT_DROP.value:
            board.move(0, 1)

    def tick(self):
        for board in self.players.values():
            board.move(0, 1)

    def get_full_state(self) -> dict:
        return {pid: board.get_state() for pid, board in self.players.items()}



class TetrisServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.session = GameSession()
        self.clients = {} 
        self.lock = asyncio.Lock()

    async def handle_client(self, reader, writer):
        player_id = f"user_{secrets.token_hex(4)}"
        print(f"New connection: {player_id}")
        
        try:
            async with self.lock:
                if not self.session.add_player(player_id):
                    writer.close()
                    return
                self.clients[writer] = player_id
                if len(self.clients) == MAX_PLAYERS:
                    self.session.is_active = True

            while True:
                data = await reader.read(1024)
                if not data:
                    break

                try:
                    message = json.loads(data.decode())
                    
                    if not SecurityProvider.verify_payload(message.get('data', {}), message.get('sig', '')):
                        print(f"Invalid signature from {player_id}")
                        continue
                    
                    cmd = message['data'].get('command')
                    async with self.lock:
                        self.session.process_input(player_id, cmd)
                except (json.JSONDecodeError, KeyError):
                    continue

        finally:
            async with self.lock:
                if writer in self.clients:
                    del self.clients[writer]
            writer.close()
            print(f"Connection closed: {player_id}")

    async def broadcast_state(self):
        while True:
            await asyncio.sleep(TICK_RATE)
            async with self.lock:
                if self.session.is_active:
                    self.session.tick()
                    state = self.session.get_full_state()
                    payload = {"type": "STATE_UPDATE", "data": state}
                    signed_payload = {
                        "data": payload,
                        "sig": SecurityProvider.sign_payload(payload),
                        "ts": time.time()
                    }
                    encoded_msg = json.dumps(signed_payload).encode()
                    
                    
                    for writer in list(self.clients.keys()):
                        try:
                            writer.write(encoded_msg)
                            await writer.drain()
                        except:
                            del self.clients[writer]

    async def run(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server listening on {self.host}:{self.port}")
        async with server:
            await asyncio.gather(server.serve_forever(), self.broadcast_state())



class TetrisClient:
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    async def send_command(self, writer, command: Command):
        payload = {"command": command.value, "nonce": secrets.token_hex(8)}
        msg = {
            "data": payload,
            "sig": SecurityProvider.sign_payload(payload)
        }
        writer.write(json.dumps(msg).encode())
        await writer.drain()

    async def start(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        print("Connected to authoritative server.")
        
        async def listen():
            while True:
                data = await reader.read(4096)
                if not data: break
                
                

        await asyncio.gather(listen())



if __name__ == "__main__":
    
    
    
    
    
    
    
    
    
    
    
    
    
    print("Tetris Architectural Framework Initialized.")
    print("Deploy TetrisServer for production-grade authoritative hosting.")
    
    
    try:
        asyncio.run(TetrisServer().run())
    except KeyboardInterrupt:
        pass