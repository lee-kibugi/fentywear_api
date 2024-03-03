from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User
from flask import Flask

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@jwt_required()
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200
