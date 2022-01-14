#-*- coding:utf-8 -*-
#从flask包中导入Flask类
from flask import Flask,render_template
#导入自定义类配置模块
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


#创建Flask实例
app = Flask(__name__)
#print("测试谁在使用包:",__name__)
#使用app.config.from_config()方法得到app的配置
app.config.from_object(Config)
#创建数据库实例
db = SQLAlchemy(app)
#创建迁移对象
migrate = Migrate(app,db)

login = LoginManager(app)
login.login_view = 'login'

#从app包中导入routes模块
from app import routes
from app import forms
from app import models
