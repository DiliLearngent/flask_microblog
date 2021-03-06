#-*- coding:utf-8 -*-
#导入模块
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import SubmitField,PasswordField,StringField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,Length
from app.models import User
# from email_validator import validate_email

#登陆表单类
class LoginForm(FlaskForm):
    username = StringField('Usename',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


#注册表单类
class RegisterForm(FlaskForm):
    username = StringField('User',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    #wtform版本原因
    #email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    #定义两个验证函数
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Please use a different email address.')

#请求重置密码表单
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    submit = SubmitField('Request Reset Password')

#重置密码表单
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Requeset Password Reset')

#个人资料编辑类表单
class EditProfileForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    about_me = TextAreaField('About_me',validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')

    #验证用户名
    def __init__(self, original_username,*args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self,username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

#Empty form for following and unfollowing
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something',validators=[DataRequired(),Length(min=1,max=140)])
    submit = SubmitField('Submit')
    

