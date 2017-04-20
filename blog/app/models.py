# -*- coding:utf-8 -*-

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    description = db.Column(db.String(360))
    blogs = db.relationship('Blog', backref='User', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def login_check(cls, username, password):
        user = cls.query.filter(db.or_(User.email == username, User.username == username)).first()
        if not user:
            return None
        if user.password != password:
            return None
        return user

    def __repr__(self):
        return '<username %r>' % self.username


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(120), db.ForeignKey('users.username'))
    blogcontent = db.Column(db.Text)
    blogtitle = db.Column(db.String)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<bolg %r>' % self.blogtitle
