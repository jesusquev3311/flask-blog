from models.db import db


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    meta_title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    @classmethod
    def create(cls, category: dict):
        category = Category(
            title=category["title"],
            meta_title=category["title"],
            meta_title=category["meta_title"],
            slug=category["slug"],
            content=category["content"],
        )
        return category.save()

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
            "parent_id": self.parent_id,
            "title": self.title,
            "meta_title": self.meta_title,
            "slug": self.slug,
            "content": self.content,
        }