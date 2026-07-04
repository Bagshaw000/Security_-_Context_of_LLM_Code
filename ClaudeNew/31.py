import asyncio
import hashlib
import hmac
import json
import logging
import os
import secrets
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from functools import wraps
import ssl
import socket

import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import bcrypt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GamePiece(Enum):
    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"


class GameState(Enum):
    WAITING = "WAITING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


class PlayerRole(Enum):
    HOST = "HOST"
    GUEST1 = "GUEST1"
    GUEST2 = "GUEST2"


@dataclass
class Coordinates:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class PieceState:
    piece_type: GamePiece
    position: Coordinates
    rotation: int
    timestamp: float = field(default_factory=time.time)

    def to_dict(self):
        return {
            'piece_type': self.piece_type.value,
            'position': {'x': self.position.x, 'y': self.position.y},
            'rotation': self.rotation,
            'timestamp': self.timestamp
        }


@dataclass
class PlayerGameState:
    player_id: str
    board: List[List[int]]
    current_piece: Optional[PieceState]
    score: int
    lines_cleared: int
    game_state: GameState
    last_update: float = field(default_factory=time.time)

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'board': self.board,
            'current_piece': self.current_piece.to_dict() if self.current_piece else None,
            'score': self.score,
            'lines_cleared': self.lines_cleared,
            'game_state': self.game_state.value,
            'last_update': self.last_update
        }


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = {}
        self.lock = threading.RLock()

    def is_allowed(self, identifier: str) -> bool:
        with self.lock:
            now = time.time()
            if identifier not in self.requests:
                self.requests[identifier] = deque()

            request_times = self.requests[identifier]
            while request_times and request_times[0] < now - self.window_seconds:
                request_times.popleft()

            if len(request_times) < self.max_requests:
                request_times.append(now)
                return True
            return False

    def cleanup_old_entries(self, max_age_seconds: int = 3600):
        with self.lock:
            now = time.time()
            identifiers_to_remove = []
            for identifier, request_times in self.requests.items():
                if request_times and request_times[-1] < now - max_age_seconds:
                    identifiers_to_remove.append(identifier)
            for identifier in identifiers_to_remove:
                del self.requests[identifier]


class AuthenticationManager:
    def __init__(self, secret_key: str, token_expiry_hours: int = 24):
        self.secret_key = secret_key
        self.token_expiry_hours = token_expiry_hours
        self.password_hasher = bcrypt.hashpw
        self.users: Dict[str, Dict] = {}
        self.sessions: Dict[str, Dict] = {}
        self.lock = threading.RLock()
        self.revoked_tokens: Set[str] = set()

    def hash_password(self, password: str) -> str:
        if not isinstance(password, bytes):
            password = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password, salt).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        if not isinstance(password, bytes):
            password = password.encode('utf-8')
        if not isinstance(hashed, bytes):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password, hashed)

    def sanitize_username(self, username: str) -> Optional[str]:
        if not isinstance(username, str):
            return None
        username = username.strip()
        if not (3 <= len(username) <= 32):
            return None
        if not all(c.isalnum() or c in '_-' for c in username):
            return None
        return username

    def sanitize_password(self, password: str) -> Optional[str]:
        if not isinstance(password, str):
            return None
        if not (8 <= len(password) <= 128):
            return None
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@
        if not (has_upper and has_lower and has_digit and has_special):
            return None
        return password

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        username = self.sanitize_username(username)
        if not username:
            return False, "Invalid username"

        password = self.sanitize_password(password)
        if not password:
            return False, "Password does not meet complexity requirements"

        with self.lock:
            if username in self.users:
                return False, "Username already exists"

            user_id = str(uuid.uuid4())
            self.users[username] = {
                'user_id': user_id,
                'password_hash': self.hash_password(password),
                'created_at': datetime.utcnow().isoformat(),
                'account_locked': False,
                'failed_attempts': 0
            }
            logger.info(f"User registered: {username}")
            return True, user_id

    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[str], str]:
        username = self.sanitize_username(username)
        if not username:
            return False, None, "Invalid username format"

        with self.lock:
            if username not in self.users:
                logger.warning(f"Authentication failed: unknown user {username}")
                return False, None, "Invalid credentials"

            user = self.users[username]

            if user.get('account_locked', False):
                return False, None, "Account is locked"

            if not self.verify_password(password, user['password_hash']):
                user['failed_attempts'] = user.get('failed_attempts', 0) + 1
                if user['failed_attempts'] >= 5:
                    user['account_locked'] = True
                    logger.warning(f"Account locked due to failed attempts: {username}")
                    return False, None, "Account locked due to multiple failed attempts"
                return False, None, "Invalid credentials"

            user['failed_attempts'] = 0
            user_id = user['user_id']

        token = self._create_token(user_id, username)
        return True, user_id, token

    def _create_token(self, user_id: str, username: str) -> str:
        payload = {
            'user_id': user_id,
            'username': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            'jti': str(uuid.uuid4())
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> Tuple[bool, Optional[str], str]:
        try:
            if token in self.revoked_tokens:
                return False, None, "Token has been revoked"

            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return True, payload['user_id'], "Token valid"
        except jwt.ExpiredSignatureError:
            return False, None, "Token expired"
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return False, None, "Invalid token"

    def revoke_token(self, token: str):
        with self.lock:
            self.revoked_tokens.add(token)

    def logout(self, token: str):
        self.revoke_token(token)
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            logger.info(f"User logged out: {payload.get('username')}")
        except jwt.InvalidTokenError:
            pass


class GameBoard:
    WIDTH = 10
    HEIGHT = 20
    EMPTY = 0

    PIECE_SHAPES = {
        GamePiece.I: [(0, 0), (1, 0), (2, 0), (3, 0)],
        GamePiece.O: [(0, 0), (1, 0), (0, 1), (1, 1)],
        GamePiece.T: [(0, 0), (1, 0), (2, 0), (1, 1)],
        GamePiece.S: [(1, 0), (2, 0), (0, 1), (1, 1)],
        GamePiece.Z: [(0, 0), (1, 0), (1, 1), (2, 1)],
        GamePiece.J: [(0, 0), (0, 1), (1, 1), (2, 1)],
        GamePiece.L: [(2, 0), (0, 1), (1, 1), (2, 1)],
    }

    def __init__(self):
        self.board = [[self.EMPTY for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.lock = threading.RLock()

    def can_place_piece(self, piece_type: GamePiece, position: Coordinates, rotation: int) -> bool:
        with self.lock:
            shape = self.PIECE_SHAPES[piece_type]
            for dx, dy in shape:
                x = position.x + dx
                y = position.y + dy

                if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
                    return False

                if self.board[y][x] != self.EMPTY:
                    return False

            return True

    def place_piece(self, piece_type: GamePiece, position: Coordinates, rotation: int) -> bool:
        with self.lock:
            if not self.can_place_piece(piece_type, position, rotation):
                return False

            shape = self.PIECE_SHAPES[piece_type]
            for dx, dy in shape:
                x = position.x + dx
                y = position.y + dy
                self.board[y][x] = 1

            return True

    def clear_lines(self) -> int:
        with self.lock:
            lines_cleared = 0
            rows_to_clear = []

            for i in range(self.HEIGHT):
                if all(cell != self.EMPTY for cell in self.board[i]):
                    rows_to_clear.append(i)
                    lines_cleared += 1

            for i in sorted(rows_to_clear, reverse=True):
                del self.board[i]
                self.board.insert(0, [self.EMPTY for _ in range(self.WIDTH)])

            return lines_cleared

    def get_board_state(self) -> List[List[int]]:
        with self.lock:
            return [row[:] for row in self.board]

    def reset(self):
        with self.lock:
            self.board = [[self.EMPTY for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]


class GameLogic:
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.board = GameBoard()
        self.current_piece: Optional[PieceState] = None
        self.score = 0
        self.lines_cleared = 0
        self.game_state = GameState.WAITING
        self.lock = threading.RLock()
        self.last_piece_time = time.time()

    def spawn_piece(self) -> bool:
        with self.lock:
            import random
            piece_type = random.choice(list(GamePiece))
            position = Coordinates(x=3, y=0)
            rotation = 0

            if self.board.can_place_piece(piece_type, position, rotation):
                self.current_piece = PieceState(
                    piece_type=piece_type,
                    position=position,
                    rotation=rotation
                )
                return True
            return False

    def move_piece_left(self) -> bool:
        with self.lock:
            if not self.current_piece:
                return False

            new_position = Coordinates(
                x=self.current_piece.position.x - 1,
                y=self.current_piece.position.y
            )

            if self.board.can_place_piece(self.current_piece.piece_type, new_position, self.current_piece.rotation):
                self.current_piece.position = new_position
                return True
            return False

    def move_piece_right(self) -> bool:
        with self.lock:
            if not self.current_piece:
                return False

            new_position = Coordinates(
                x=self.current_piece.position.x + 1,
                y=self.current_piece.position.y
            )

            if self.board.can_place_piece(self.current_piece.piece_type, new_position, self.current_piece.rotation):
                self.current_piece.position = new_position
                return True
            return False

    def move_piece_down(self) -> bool:
        with self.lock:
            if not self.current_piece:
                return False

            new_position = Coordinates(
                x=self.current_piece.position.x,
                y=self.current_piece.position.y + 1
            )

            if self.board.can_place_piece(self.current_piece.piece_type, new_position, self.current_piece.rotation):
                self.current_piece.position = new_position
                return True
            return False

    def lock_piece(self) -> bool:
        with self.lock:
            if not self.current_piece:
                return False

            if self.board.place_piece(
                self.current_piece.piece_type,
                self.current_piece.position,
                self.current_piece.rotation
            ):
                lines_cleared = self.board.clear_lines()
                self.lines_cleared += lines_cleared
                self.score += lines_cleared