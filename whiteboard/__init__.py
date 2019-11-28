from os import environ
from flask import Flask
from whiteboard import settings as wbs

assert isinstance(wbs.CAMPUS_CARD, wbs.CampusCard) and isinstance(wbs.ACADEMIC_TERM, wbs.AcademicTerm)
assert wbs.DEPT_ABBREV_LEN > 0 and wbs.COURSE_CODE_LEN > 0 and wbs.CLASS_SECTION_LEN > 0


def create_app():
    app = Flask(__name__)
    app.config.from_object('whiteboard.config.ProductionConfig' if environ.get('FLASK_ENV') == 'production' else 'whiteboard.config.DevelopmentConfig')
    app.config.from_pyfile('settings.py')

    with app.app_context():
        from whiteboard.models import db, login_manager
        db.init_app(app)
        db.create_all()
        login_manager.init_app(app)

        from whiteboard.views import csrf
        csrf.init_app(app)

        from whiteboard.views.exceptions import exceptions as exceptions_blueprint
        app.register_blueprint(exceptions_blueprint)

        from whiteboard.views.root import root as root_blueprint
        app.register_blueprint(root_blueprint)

        from whiteboard.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from whiteboard.views.academics import academics as academics_blueprint
        app.register_blueprint(academics_blueprint)

        from whiteboard.views.classes import classes as classes_blueprint
        app.register_blueprint(classes_blueprint)

        return app
