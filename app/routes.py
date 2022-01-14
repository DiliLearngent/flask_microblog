#-*- coding:utf-8 -*-
#从app包中导入app这个实例
from flask import render_template,flash,redirect,url_for,request
from werkzeug.urls import url_parse
from app import app,db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user,login_user,logout_user,login_required

from app.models import User

#2个路由
@app.route('/')
@app.route('/index')
@login_required
#一个视图函数
#首页视图
def index():
    # user = {'username':'lsy'}
    # posts = [
    #     {
    #         'author':{'username':'jhon'},
    #         'body':'this is a good day!'
    #     },
    #     {
    #         'author':{'username':'lucy'},
    #         'body':'nice to meet you!'
    #     }
    # ]
    #return render_template('index.html',title='Home',user=user,posts=posts)
    return render_template('index.html',title='Home')

#用户登陆视图
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        #flash('Login request for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
        #return redirect(url_for('index'))
        #重定向到next页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign in',form=form)

#用户退出视图
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#用户注册视图
@app.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)