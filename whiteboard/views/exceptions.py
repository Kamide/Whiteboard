from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

exceptions = Blueprint('exceptions', __name__, template_folder='../templates/exceptions')


@exceptions.app_errorhandler(HTTPException)
def handle_http_exception(e):
    return render_template('http-exception.html', title=f'{e.code} {e.name}', message=e.description), e.code
