from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=db.func.current_timestamp()
    )

    @classmethod
    def create(cls, user: dict):
        user = User(
            name=user["name"],
            username=user["username"],
            email=user["email"],
            password=user["password"],
            description=user["description"]
        )
        return user.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            print(f"error: {e}")
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(f"error: {e}")

    def update(self):
        self.save()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "description": self.description,
            "created_at": self.created_at
        }
