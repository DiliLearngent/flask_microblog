from flask import render_template
from flask_mail import Message
from app import mail
from app import app
from threading import Thread

#异步发送电子邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(subject,sender,recipients,text_body,html_body):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    Thread(target=send_async_email,args=(app,msg)).start()

#发送密码重置电子邮件函数
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[Microblog] Reset Your Password',
    sender=app.config['MAIL_USERNAME'],recipients=[user.email],
    text_body=render_template('mail/reset_password.txt',user=user,token=token),
    html_body = render_template('mail/reset_password.html',user=user,token=token))
    