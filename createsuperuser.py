from datetime import datetime
from getpass import getpass
from re import match
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from whiteboard import create_app
from whiteboard.models import Teacher, User
from whiteboard.settings import CAMPUS_CARD

while True:
    username = input(f'* Username ({CAMPUS_CARD}): ')
    if not username:
        print('  - Username is required.')
    elif len(username) < CAMPUS_CARD.min_len or len(username) > CAMPUS_CARD.max_len:
        print('  - Invalid username length, please try again.')
    elif not match('^[^\\W_]+$', username):
        print('  - Username is restricted to word characters, please try again.')
    else:
        break

while True:
    while True:
        password = getpass('* Password: ')
        if not password:
            print('  - Password is required.')
        else:
            break
    password_confirmation = getpass('* Password Confirmation: ')
    if password_confirmation != password:
        print('  - Passwords do not match, please try again.')
    else:
        break

while True:
    full_name = input('* Full Name: ')
    if not full_name:
        print('  - Full name is required.')
    else:
        break

display_name = input('  Display Name: ')

while True:
    email = input('* Email Address: ')
    if not match('[^@]+@[^@]+\\.[^@]+', email):
        print('  - Invalid email address, please try again.')
    else:
        break

app = create_app()
db = SQLAlchemy(app)

new_user = User(username=username.upper(), password=generate_password_hash(password), full_name=full_name, display_name=display_name, email=email.lower(), join_date=datetime.utcnow())
db.session.add(new_user)
db.session.flush()

new_teacher = Teacher(user_id=new_user.id)
db.session.add(new_teacher)
db.session.commit()
