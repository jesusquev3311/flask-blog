from flask import jsonify
from utils.password import  check_password
from models import User

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password(password):
        return user
    
    return jsonify({"message": "User not Found"}), 404

def identity(payload):
    user_id = payload["user_id"]

    if user_id != None:
        return User.query.filter_by(id=user_id)
    else:
        return jsonify({"message": "User not Found"}), 404