import boto3
import hashlib
import os
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import unittest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def generate_key():
    return Fernet.generate_key()


def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


db.create_all()


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401


@app.route('/transaction', methods=['POST'])
def transaction():
    key = os.environ.get('ENCRYPTION_KEY').encode()
    transaction_data = request.json['data']
    encrypted_data = encrypt_data(transaction_data, key)
    
    return jsonify({"encrypted_data": encrypted_data.decode()}), 200


class TestATMController(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register(self):
        response = self.app.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.app.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    app.run(debug=True)