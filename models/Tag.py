from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    meta_title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    @classmethod
    def create(cls, tag: dict):
        tag = Tag(
            title=tag["title"],
            meta_title=tag["meta_title"],
            slug=tag["slug"],
            content=tag["content"],
        )
        return tag.save()

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
            "title": self.title,
            "meta_title": self.meta_title,
            "slug": self.slug,
            "content": self.content,
        }