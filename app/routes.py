#-*- coding:utf-8 -*-
#从app包中导入app这个实例
from datetime import datetime
from flask import render_template,flash,redirect,url_for,request
from sqlalchemy import false
from werkzeug.urls import url_parse
from app import app,db
from app import email
from app.forms import LoginForm, RegisterForm,EditProfileForm,EmptyForm,PostForm,ResetPasswordRequestForm,ResetPasswordForm
from flask_login import current_user,login_user,logout_user,login_required
# from flask_sqlalchemy import Pagination

from app.models import User,Post
from app.email import send_password_reset_email

#2个路由
@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
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
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page',1,int)
    # posts = current_user.followed_posts().all()
    posts = current_user.followed_posts().paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index',page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title='Home Page',form=form,posts=posts.items,next_url=next_url,prev_url=prev_url)

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

#用户个人资料视图
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author':user, 'body':'Test post #1'},
    #     {'author':user, 'body':'Test post #2'}
    # ]
    form = EmptyForm()
    page = request.args.get('page',1,int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('user',username=username,page=posts.next_num) if posts.has_next else None
    prev_url  = url_for('user',username=username,page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html',user=user,posts=posts.items,form=form,next_url=next_url,prev_url=prev_url)

#记录访问时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


#编辑个人资料视图函数
@app.route('/edit_profile',methods = ['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile',form=form)

#关注
@app.route('/follow/<username>',methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user',username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user',username=username))
    else:
        return redirect(url_for('index'))


#取消关注
@app.route('/unfollow/<username>',methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user',username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user',username=username))
    else:
        return redirect(url_for('index'))

#轻松地找到用户和关注
@app.route('/explore')
@login_required
def explore():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page',1,int)
    posts = current_user.followed_posts().paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('explore',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore',page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title='Explore',posts=posts.items,next_url=next_url,prev_url=prev_url)


#密码重置视图函数
@app.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('request_reset_password.html',title='Reset Password',form=form)


#重置用户密码
@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    print('2222')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html',form=form)
    
    


