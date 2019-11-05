from setuptools import setup

setup(
    name='whiteboard',
    packages=['whiteboard'],
    include_package_data=True,
    install_requires=[
        'flask >= 1.1.1',
        'flask-login >= 0.4.1',
        'flask-sqlalchemy >= 2.4.0',
        'flask-wtf >= 0.14.2',
    ],
)
