from flask import jsonify
from flask_sqlalchemy import session
from utils.password import  check_password
from models.User import User

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    print(f"USER: {user}")

    if user and check_password(password, user.password):
        return user
    
    return jsonify({"message": "User not Found"}), 404

def identity(payload):
    user_id = payload["identity"]

    if user_id != None:
        return User.query.filter_by(id=user_id)
    else:
        return jsonify({"message": "User not Found"}), 404