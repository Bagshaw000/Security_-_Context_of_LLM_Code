import os
import json
import logging
import unittest
import boto3
from datetime import datetime
from flask import Flask, request, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(32).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


ENCRYPTION_KEY = os.environ.get('DATA_ENCRYPTION_KEY', Fernet.generate_key().decode())
cipher_suite = Fernet(ENCRYPTION_KEY.encode())


s3_client = boto3.client('s3', region_name='us-east-1')
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
S3_BUCKET_NAME = 'user-interaction-logs-storage'
KINESIS_STREAM_NAME = 'user-analytics-stream'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=150)])
    password = PasswordField('Password', [validators.DataRequired()])

class InteractionForm(FlaskForm):
    event_type = StringField('Event Type', [validators.DataRequired(), validators.Length(max=50)])
    element_id = StringField('Element ID', [validators.DataRequired(), validators.Length(max=100)])
    metadata = StringField('Metadata', [validators.Length(max=500)])


def encrypt_data(data: str) -> str:
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return cipher_suite.decrypt(token.encode()).decode()

def upload_to_s3(data, filename):
    try:
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=json.dumps(data))
    except ClientError as e:
        logger.error(f"AWS S3 Error: {e}")

def send_to_analytics(data):
    try:
        kinesis_client.put_record(
            StreamName=KINESIS_STREAM_NAME,
            Data=json.dumps(data),
            PartitionKey=str(data.get('user_id', 'anonymous'))
        )
    except ClientError as e:
        logger.error(f"AWS Kinesis Error: {e}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            logger.info(f"User {user.username} logged in successfully.")
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"error": "Validation failed", "details": form.errors}), 400

@app.route('/track', methods=['POST'])
@login_required
def track_interaction():
    form = InteractionForm()
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid interaction data", "details": form.errors}), 400

    interaction_data = {
        "user_id": current_user.id,
        "username_encrypted": encrypt_data(current_user.username),
        "event_type": form.event_type.data,
        "element_id": form.element_id.data,
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": request.remote_addr
    }

    
    upload_to_s3(interaction_data, f"interactions/{current_user.id}_{datetime.utcnow().timestamp()}.json")
    send_to_analytics(interaction_data)

    return jsonify({"status": "Interaction recorded"}), 200

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 error: {request.path}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "An internal error occurred"}), 500


class SecurityAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            user = User(username='testuser')
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()

    def test_login_success(self):
        response = self.app.post('/login', data=dict(username='testuser', password='SecurePass123!'))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        response = self.app.post('/track', data=dict(event_type='click', element_id='btn-1'))
        self.assertEqual(response.status_code, 401)

    def test_encryption_logic(self):
        original = "sensitive_data"
        encrypted = encrypt_data(original)
        self.assertNotEqual(original, encrypted)
        self.assertEqual(original, decrypt_data(encrypted))


if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
    
    
    if os.environ.get('RUN_TESTS') == '1':
        unittest.main()
    else:
        
        app.run(ssl_context='adhoc', port=5000)