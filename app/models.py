#-*- coding:utf-8 -*-
from app import db
from datetime import datetime
#导入密码哈希值计算和验证函数库
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

@login.user_loader
def load_user(id):
        return User.query.get(int(id))

#关注者关联表
followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
)

#用户表
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(128),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    #更新字段
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    followed = db.relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id==id),
        secondaryjoin = (followers.c.followed_id==id),
        backref = db.backref('followers',lazy='dynamic'),
        lazy='dynamic'
    )


    def __repr__(self) -> str:
        #return '<User {}>'.format(self.username)
        return '<User {}, Email {}, Password_Hash {}, Posts {}'.format(self.username, self.email, self.password_hash, self.posts)
    
    #根据用户输入计算哈希值存入密码字段
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    #用户输入的密码与数据库中的hash值进行判断
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #定义用户头像函数
    def avatar(self,size):
        #邮箱号的hash值
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://cravatar.cn/avatar/{}?d=identicon&s={}'.format(digest,size)

    #检查两个用户是否已经存在关系
    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    #添加关注者
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
    
    #删除关注者
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    # #已关注用户的帖子的查询
    # def followed_posts(self):
    #     return Post.query.join(
    #         followers, (followers.c.followed_id==Post.user_id)).filter(
    #             followers.c.follower_id==self.id).order_by(
    #                 Post.timestamp.desc())
    
    #结合自己和关注者的照片
    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

#帖子表
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.body)