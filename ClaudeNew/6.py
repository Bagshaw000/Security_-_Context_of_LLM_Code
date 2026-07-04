import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from functools import wraps
import secrets
import string

import psycopg2
from psycopg2 import sql, Error
import bcrypt
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bicycle_shop.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.ssl_mode = os.getenv('DB_SSL_MODE', 'require')

        if not all([self.host, self.database, self.user, self.password]):
            raise ValueError("Missing required database configuration environment variables")


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                sslmode=self.config.ssl_mode
            )
            logger.info("Database connection established successfully")
            return self.connection
        except Error as e:
            logger.error(f"Database connection failed: {str(e)[:100]}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                self.connection.commit()
                return []
        except Error as e:
            self.connection.rollback()
            logger.error(f"Query execution failed: {str(e)[:100]}")
            raise
        finally:
            cursor.close()

    def execute_update(self, query: str, params: tuple = None) -> int:
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            rows_affected = cursor.rowcount
            logger.info(f"Query executed successfully. Rows affected: {rows_affected}")
            return rows_affected
        except Error as e:
            self.connection.rollback()
            logger.error(f"Update execution failed: {str(e)[:100]}")
            raise
        finally:
            cursor.close()


class InputValidator:
    MAX_STRING_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 5000
    MIN_PASSWORD_LENGTH = 12
    
    @staticmethod
    def validate_email(email: str) -> bool:
        if not email or len(email) > InputValidator.MAX_STRING_LENGTH:
            return False
        if '@' not in email or '.' not in email.split('@')[-1]:
            return False
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < InputValidator.MIN_PASSWORD_LENGTH:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c in string.punctuation for c in password):
            return False
        return True

    @staticmethod
    def validate_string(value: str, max_length: int = MAX_STRING_LENGTH) -> bool:
        if not isinstance(value, str):
            return False
        if len(value) == 0 or len(value) > max_length:
            return False
        return True

    @staticmethod
    def validate_positive_number(value: float) -> bool:
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_integer(value: int) -> bool:
        try:
            int(value)
            return value >= 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def sanitize_string(value: str) -> str:
        if not isinstance(value, str):
            return ""
        return value.strip()[:InputValidator.MAX_STRING_LENGTH]


class PasswordManager:
    HASH_ROUNDS = 12

    @staticmethod
    def hash_password(password: str) -> str:
        if not InputValidator.validate_password(password):
            raise ValueError("Password does not meet security requirements")
        salt = bcrypt.gensalt(rounds=PasswordManager.HASH_ROUNDS)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {str(e)[:100]}")
            return False

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))


class BicycleShopDatabase:
    def __init__(self, db_config: DatabaseConfig):
        self.db = DatabaseConnection(db_config)
        self.db.connect()

    def create_schema(self):
        schema_queries = [
            sql.SQL(),
            sql.SQL(),
            sql.SQL(),
            sql.SQL(),
            sql.SQL(),
            sql.SQL(),
            sql.SQL(),
            sql.SQL(),
            sql.SQL()
        ]

        for query in schema_queries:
            try:
                self.db.execute_update(query.as_string(self.db.connection))
                logger.info("Schema created successfully")
            except Error as e:
                logger.error(f"Schema creation error: {str(e)[:100]}")
                raise

    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> int:
        if not InputValidator.validate_email(email):
            raise ValueError("Invalid email format")
        if not InputValidator.validate_password(password):
            raise ValueError("Password does not meet security requirements")
        if not InputValidator.validate_string(first_name):
            raise ValueError("Invalid first name")
        if not InputValidator.validate_string(last_name):
            raise ValueError("Invalid last name")

        first_name = InputValidator.sanitize_string(first_name)
        last_name = InputValidator.sanitize_string(last_name)
        email = email.lower().strip()
        password_hash = PasswordManager.hash_password(password)

        query = 
        
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(query, (email, password_hash, first_name, last_name))
            self.db.connection.commit()
            user_id = cursor.fetchone()[0]
            logger.info(f"User created successfully. User ID: {user_id}")
            self._log_audit("user_created", "users", user_id, f"User {email} created")
            return user_id
        except Error as e:
            self.db.connection.rollback()
            if "unique constraint" in str(e).lower():
                logger.warning(f"Duplicate email registration attempt: {email[:20]}...")
                raise ValueError("Email already exists")
            logger.error(f"User creation failed: {str(e)[:100]}")
            raise
        finally:
            cursor.close()

    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        if not InputValidator.validate_email(email):
            logger.warning(f"Invalid email format in login attempt: {email[:20]}...")
            return None

        email = email.lower().strip()
        query = 
        
        try:
            results = self.db.execute_query(query, (email,))
            if not results:
                logger.warning(f"Login attempt for non-existent user: {email[:20]}...")
                return None
            
            user = results[0]
            if PasswordManager.verify_password(password, user['password_hash']):
                logger.info(f"User authenticated successfully. User ID: {user['user_id']}")
                self._log_audit("user_authenticated", "users", user['user_id'], "User logged in")
                return {
                    'user_id': user['user_id'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            else:
                logger.warning(f"Failed authentication attempt for user: {email[:20]}...")
                return None
        except Error as e:
            logger.error(f"Authentication error: {str(e)[:100]}")
            return None

    def create_product(self, product_name: str, description: str, price: float, 
                      stock_quantity: int, category: str) -> int:
        if not InputValidator.validate_string(product_name):
            raise ValueError("Invalid product name")
        if not InputValidator.validate_string(description, InputValidator.MAX_DESCRIPTION_LENGTH):
            raise ValueError("Invalid description")
        if not InputValidator.validate_positive_number(price):
            raise ValueError("Invalid price")
        if not InputValidator.validate_integer(stock_quantity):
            raise ValueError("Invalid stock quantity")
        if not InputValidator.validate_string(category):
            raise ValueError("Invalid category")

        product_name = InputValidator.sanitize_string(product_name)
        description = InputValidator.sanitize_string(description)
        category = InputValidator.sanitize_string(category)

        query = 
        
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(query, (product_name, description, price, stock_quantity, category))
            self.db.connection.commit()
            product_id = cursor.fetchone()[0]
            logger.info(f"Product created successfully. Product ID: {product_id}")
            self._log_audit("product_created", "products", product_id, f"Product {product_name} created")
            return product_id
        except Error as e:
            self.db.connection.rollback()
            logger.error(f"Product creation failed: {str(e)[:100]}")
            raise
        finally:
            cursor.close()

    def get_product(self, product_id: int) -> Optional[Dict]:
        if not InputValidator.validate_integer(product_id):
            raise ValueError("Invalid product ID")

        query = 
        
        try:
            results = self.db.execute_query(query, (product_id,))
            return results[0] if results else None
        except Error as e:
            logger.error(f"Product retrieval failed: {str(e)[:100]}")
            return None

    def update_product(self, product_id: int, product_name: str = None, description: str = None,
                      price: float = None, stock_quantity: int = None, category: str = None) -> bool:
        if not InputValidator.validate_integer(product_id):
            raise ValueError("Invalid product ID")

        updates = {}
        if product_name is not None:
            if not InputValidator.validate_string(product_name):
                raise ValueError("Invalid product name")
            updates['product_name'] = InputValidator.sanitize_string(product_name)
        
        if description is not None:
            if not InputValidator.validate_string(description, InputValidator.MAX_DESCRIPTION_LENGTH):
                raise ValueError("Invalid description")
            updates['description'] = InputValidator.sanitize_string(description)
        
        if price is not None:
            if not InputValidator.validate