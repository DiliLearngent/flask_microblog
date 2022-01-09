#-*- coding:utf-8 -*-
#从flask包中导入Flask类
from flask import Flask,render_template
#导入自定义类配置模块
from config import Config

#创建Flask实例
app = Flask(__name__)
#print("测试谁在使用包:",__name__)
#使用app.config.from_config()方法得到app的配置
app.config.from_object(Config)

#从app包中导入routes模块
from app import routes
from app import forms
