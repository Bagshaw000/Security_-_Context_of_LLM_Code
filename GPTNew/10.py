from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_streaming.db'
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    devices = db.relationship('Device', backref='owner', lazy=True)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class DeviceSchema(Schema):
    device_name = fields.Str(required=True)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/device', methods=['POST'])
@jwt_required()
def register_device():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    schema = DeviceSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_device = Device(device_name=data['device_name'], user_id=current_user_id)
    db.session.add(new_device)
    db.session.commit()
    return jsonify({"msg": "Device registered successfully"}), 201

@app.route('/devices', methods=['GET'])
@jwt_required()
def get_devices():
    current_user_id = get_jwt_identity()
    devices = Device.query.filter_by(user_id=current_user_id).all()
    return jsonify([{"id": device.id, "device_name": device.device_name} for device in devices]), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)