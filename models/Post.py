from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, primary_key=False)
    title = db.Column(db.String(255), nullable=False)
    meta_title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.String(255), nullable=True)
    published = db.Column(db.Boolean(False), nullable=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(), 
        nullable=False,
        default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime(), 
        nullable=False,
        default=db.func.current_timestamp()
    )

    @classmethod
    def create(cls, post: dict):
        post = Post(
            user_id=post["user_id"],
            title=post["title"],
            meta_title=post["meta_title"],
            slug=post["slug"], 
            summary=post["summary"],
            meta_description=post["meta_description"],
            published=post["published"] 
        )
        return post.save()

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
            "user_id": self.user_id,
            "title": self.title,
            "meta_title": self.meta_title,
            "slug": self.slug,
            "summary": self.summary,
            "meta_description": self.meta_description,
            "published": self.published
        }


class Post_category(db.Model):
    __tablename__ = "post_category"
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger, primary_key=False)
    category_id = db.Column(db.BigInteger, primary_key=False)


class Post_comment(db.Model):
    __tablename__ = "post_comment"
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger, primary_key=False)
    author = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean(False), nullable=True)
    created_at = db.Column(
        db.DateTime(), 
        nullable=False,
        default=db.func.current_timestamp()
    )


class Post_tag(db.Model):
    __tablename__ = "post_tag"
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger, primary_key=False)
    tag_id = db.Column(db.BigInteger, primary_key=False)


class Post_meta(db.Model):
    __tablename__ = "post_meta"
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
