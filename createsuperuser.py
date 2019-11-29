import sqlite3
from datetime import datetime
from getpass import getpass
from re import match
from werkzeug.security import generate_password_hash
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

conn = sqlite3.connect('development.db')
c = conn.cursor()
c.execute('INSERT INTO Users (username, password, full_name, display_name, email, join_date) VALUES (?,?,?,?,?,?)', (username.upper(), generate_password_hash(password), full_name, display_name, email.lower(), datetime.utcnow()))
user_id = c.lastrowid
conn.commit()
c.execute(f'INSERT INTO Teachers (user_id) VALUES ({user_id})')
conn.commit()
c.close()
conn.close()
