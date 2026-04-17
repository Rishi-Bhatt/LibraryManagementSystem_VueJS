from functools import wraps

import bcrypt
from flask import current_app, jsonify, request
from flask_security import login_user
from itsdangerous import URLSafeTimedSerializer

from models import db, user_datastore


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(' ')[1]
            user = user_datastore.find_user(authentication_token=token)
            if user:
                login_user(user)
            else:
                return jsonify({'message': 'Invalid or expired token'}), 401
        else:
            return jsonify({'message': 'Token is missing'}), 403

        return f(*args, **kwargs)

    return decorated


def generate_auth_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps({'id': user.id})
    return token
