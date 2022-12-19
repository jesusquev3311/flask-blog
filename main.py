from flask import Flask, jsonify, request
from models import db, User
from config import config
from utils.password import secure_password

def create_app(environment) -> None:
    app = Flask(__name__)
    app.config.from_object(environment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

environment = config["development"]
app = create_app(environment)

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    users = [user.json() for user in User.query.all()]

    return jsonify({"users" : users})

@app.route("/api/v1/users/<id>", methods = ["GET"])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"message": "User doesn't exist"})
    
    return jsonify({"user" : user.json()})

@app.route("/api/v1/users", methods = ["POST"])
def create_user():
    json = request.get_json(force=True)

    if json.get("username") is None and json.get("password"):
        return jsonify({"message" : "Bad request"}), 400

    try:
        json["password"] = secure_password(json["password"])
        user = User.create(json)
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({"user" : user.json()})


@app.route("/api/v1/users/<id>", methods = ["PUT"])
def update_user(id):
    user = User.query.filter_by(id = id).first()

    if user is None:
        return jsonify({"message" : "User not found"}), 404

    json = request.get_json(force=True)
    if json.get("username") is None:
        return jsonify({"message" : "Bad request"}), 400

    user = json
    user.update()

    return jsonify({"User" : user.json()})

@app.route("/api/v1/users/<id>", methods = ["DELETE"])
def delete_user(id):
    user = User.query.filter_by(id = id).first()
    if user is None:
        return jsonify({"message" : "User not Found"}), 404
    
    user.delete()

    return jsonify({"user": user.json()})

@app.route("/api/v1/posts", methods = ["GET"])
def get_posts():
    posts = [post.json() for post in Post.query.all()]

    return jsonify({"posts" : posts})




if __name__ == "__main__":
    app.run(debug = True)