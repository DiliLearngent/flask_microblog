#-*- coding:utf-8 -*-
#从app包中导入app实例
from logging import debug
from app import app

if __name__ == "__main__":
    app.run(debug=True)