#-*- coding:utf-8 -*-
#导入模块
from flask_wtf import FlaskForm
from wtforms import SubmitField,PasswordField,StringField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usename',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

