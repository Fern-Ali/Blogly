"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import datetime

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)






class User(db.Model):
    """user model for blogly. Include: id PK, first_name, last_name, image_url"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    last_name = db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    image_url = db.Column(db.String(200),
                          nullable=True,
                          unique=False,
                          default="https://99designs-blog.imgix.net/blog/wp-content/uploads/2018/11/attachment_78456430-e1541654366936.jpeg?auto=format&q=60&fit=max&w=930")

class Post(db.Model):
    """POST model for blogly. Containing id as primary key, title, content, created_at, and user_id from USER model as FOREIGN KEY"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(79),
                      nullable=False,
                      unique=False)
    content = db.Column(db.String(1000),
                        nullable=False,
                        unique=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    image_url = db.Column(db.String(200),
                          nullable=True,
                          unique=False,
                          default="https://99designs-blog.imgix.net/blog/wp-content/uploads/2018/11/attachment_78456430-e1541654366936.jpeg?auto=format&q=60&fit=max&w=930")
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        #FIGURE OUT HOW TO ADD CASCADE. ASK PUSHPITA. FOR NOW SET NULLABLE TO TRUE SO WE CAN RESET TABLE. Ok that doesnt work anyway. figure it out later.
                        nullable=False)
    #post_user = db.relationship('Department', backref='employees')


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)



class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )
