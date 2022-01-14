#-*- coding:utf-8 -*-
from app import db
from datetime import datetime
#导入密码哈希值计算和验证函数库
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
        return User.query.get(int(id))

#用户表
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(128),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    def __repr__(self) -> str:
        #return '<User {}>'.format(self.username)
        return '<User {}, Email {}, Password_Hash {}, Posts {}'.format(self.username, self.email, self.password_hash, self.posts)
    
    #根据用户输入计算哈希值存入密码字段
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    #用户输入的密码与数据库中的hash值进行判断
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    

    

    

#帖子表
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.body)