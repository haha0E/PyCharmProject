from flask import Flask
from .main import main as main_blueprint
from .auth import auth as auth_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # 注册蓝图
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app