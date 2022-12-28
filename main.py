from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from utils.security import authenticate, identity
from models.db import db
from models.User import User
from models.Post import Post
from config import config
from utils.password import secure_password
from utils.security import authenticate, identity


def create_app(environment) -> None:
    app = Flask(__name__)
    app.secret_key = "zuztech" #just for development purpose
    app.config.from_object(environment)
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
    jwt = JWT(app, authenticate, identity)

    with app.app_context():
        print(" ** starting app...")
        db.init_app(app)
        print(" ** craating app...")
        try:
            db.create_all()
        except Exception as e:
            print(f"db error: {e}")

    return app


environment = config["development"]
app = create_app(environment)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bad Request"}), 400


@app.route("/api/v1/users", methods=["GET"])
@jwt_required()
def get_users():
    users = [user.json() for user in User.query.all()]

    return jsonify({"users": users})


@app.route("/api/v1/users/<id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"message": "User doesn't exist"})
    
    return jsonify({"user": user.json()})


@app.route("/api/v1/users", methods=["POST"])
@jwt_required()
def create_user():
    json = request.get_json(force=True)

    if json.get("username") is None and json.get("password"):
        return jsonify({"message": "Bad request"}), 400

    try:
        json["password"] = secure_password(json["password"])
        user = User.create(json)
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({"user": user.json()})


@app.route("/api/v1/users/<id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    user = User.query.filter_by(id=id).first()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    json = request.get_json(force=True)
    if json.get("username") is None:
        return jsonify({"message": "Bad request"}), 400

    user = json
    user.update()

    return jsonify({"User": user.json()})


@app.route("/api/v1/users/<id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"message": "User not Found"}), 404
    
    user.delete()

    return jsonify({"user": user.json()})


@app.route("/api/v1/posts", methods=["GET"])
@jwt_required()
def get_posts():
    posts = [post.json() for post in Post.query.all()]

    return jsonify({"posts": posts})


@app.route("/api/v1/posts", methods=["POST"])
@jwt_required()
def create_post():
    json = request.get_json(force=True)

    if json.get("title") is None and json.get("user_id") is None:
        return jsonify({"message": "Bad request"}), 400

    try:
        post = Post.create(json)
        print(post)
    except Exception as e:
        return jsonify({"message": f"error: {e} + {post}"}), 400

    return jsonify({"user": post.json()})


if __name__ == "__main__":
    app.run(debug=True)
