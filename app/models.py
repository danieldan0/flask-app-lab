from app import db
from datetime import datetime as dt

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    posted = db.Column(db.DateTime, index=True, default=dt.now())

    def __repr__(self):
        return f"<Post {self.title}>"