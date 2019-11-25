from flask import Blueprint, render_template

errorpages = Blueprint('errorpages', __name__, template_folder='../templates/errorpages')


@errorpages.app_errorhandler(403)
def page_forbidden(e):
    message = "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server."
    return render_template('error.html', title='403 Forbidden', message=message), 403


@errorpages.app_errorhandler(404)
def page_not_found(e):
    message = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
    return render_template('error.html', title='404 Not Found', message=message), 404
