import os

class Config:
    #根据环境变量设置此密钥，用来防护CSRF攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
