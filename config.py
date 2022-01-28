import os

base_dir = os.path.abspath(os.path.dirname(__file__))
class Config:
    #根据环境变量设置此密钥，用来防护CSRF攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #每个页面帖子数量配置
    POSTS_PER_PAGE = 3

