# -*- coding: utf-8 -*-
from flask import Flask,request
from application.controller.tbcapture import tbcapture as tbcapture_blueprint

application = Flask(__name__, instance_relative_config=True)	#提交前注释掉
# application = Flask(__name__)		#提交前添加
application.config.from_object('conf.default')	#默认配置
application.config.from_object('conf.config')	#私有配置
application.config.from_pyfile('config.py')	#开发环境配置		#提交前注释掉

application.register_blueprint(tbcapture_blueprint, url_prefix='/tbcapture')
if __name__ == '__main__':
  application.run(debug=application.config['DEBUG'], threaded = True, port=application.config['PORT'])