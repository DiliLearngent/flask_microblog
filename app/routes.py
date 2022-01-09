#-*- coding:utf-8 -*-
#从app包中导入app这个实例
from flask import render_template,flash,redirect,url_for
from app import app
from app.forms import LoginForm

#2个路由
@app.route('/')
@app.route('/index')
#一个视图函数
def index():
    user = {'username':'lsy'}
    posts = [
        {
            'author':{'username':'jhon'},
            'body':'this is a good day!'
        },
        {
            'author':{'username':'lucy'},
            'body':'nice to meet you!'
        }
    ]
    return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign in',form=form)
