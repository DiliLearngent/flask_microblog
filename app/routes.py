#-*- coding:utf-8 -*-
#从app包中导入app这个实例
from app import app

#2个路由
@app.route('/')
@app.route('/index')
#一个视图函数
def index():
    return '<p>Hello World!</p>'
