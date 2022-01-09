#-*- coding:utf-8 -*-
from app import db
from datetime import datetime

#用户表
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(128),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

#帖子表
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.body)