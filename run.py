from flask import Flask,request
from application.controller.tbcapture import tbcapture as tbcapture_blueprint

# app = Flask(__name__, instance_relative_config=True)
app = Flask(__name__)
app.config.from_object('conf.default')	#默认配置
app.config.from_object('conf.config')	#私有配置
# app.config.from_pyfile('config.py')	#开发环境配置

if __name__ == '__main__':
  app.register_blueprint(tbcapture_blueprint, url_prefix='/tbcapture')
  app.run(debug=app.config['DEBUG'], threaded = True, port=app.config['PORT'])