import os

base_dir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(base_dir,'microblog.env'))
class Config:
    #根据环境变量设置此密钥，用来防护CSRF攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #每个页面帖子数量配置
    POSTS_PER_PAGE = 3
    #邮件模块的配置
    ADMINS = ['your-email@example.com']

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')#客户端授权密码

