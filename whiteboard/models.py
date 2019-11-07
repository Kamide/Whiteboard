from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from whiteboard.settings import CAMPUS_CARD

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(CAMPUS_CARD.max_len, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255))
    email = db.Column(db.String(254, collation='NOCASE'), nullable=False, unique=True)
    join_date = db.Column(db.Date())

    @property
    def is_active(self):
        return self.join_date is not None
