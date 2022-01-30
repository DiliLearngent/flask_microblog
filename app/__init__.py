#-*- coding:utf-8 -*-
#从flask包中导入Flask类
import logging
from flask import Flask,render_template
#导入自定义类配置模块
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from logging.handlers import RotatingFileHandler
import os


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

mail = Mail(app)

#从app包中导入routes模块
from app import routes
from app import forms
from app import models
from app import errors

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

