from flask import Flask
from os import environ
from whiteboard import settings

assert isinstance(settings.CAMPUS_CARD, settings.CampusCard)


def create_app():
    app = Flask(__name__)
    app.config.from_object('whiteboard.config.ProductionConfig' if environ.get('FLASK_ENV') == 'production' else 'whiteboard.config.DevelopmentConfig')
    app.config.from_pyfile('settings.py')

    with app.app_context():
        from whiteboard.models import db, login_manager
        db.init_app(app)
        db.create_all()
        login_manager.init_app(app)

        from whiteboard.views.root import root as root_blueprint
        app.register_blueprint(root_blueprint)

        from whiteboard.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from whiteboard.views.management import management as management_blueprint
        app.register_blueprint(management_blueprint)

        return app
