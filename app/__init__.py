#-*- coding:utf-8 -*-
#从flask包中导入Flask类
from flask import Flask

#创建Flask实例
app = Flask(__name__)
print("测试谁在使用包:",__name__)

#从app包中导入routes模块
from app import routes
