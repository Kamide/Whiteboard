from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('whiteboard.config.ProductionConfig' if os.environ.get('FLASK_ENV') == 'production' else 'whiteboard.config.DevelopmentConfig')
    app.config.from_pyfile('settings.py')

    db.init_app(app)
    login_manager.init_app(app)

    from whiteboard.views.root import root as root_blueprint
    from whiteboard.views.auth import auth as auth_blueprint

    app.register_blueprint(root_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
