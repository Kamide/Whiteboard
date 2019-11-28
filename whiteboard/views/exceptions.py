from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

exceptions = Blueprint('exceptions', __name__, template_folder='../templates/exceptions')


class EntityNotFound(Exception):
    code = 404
    name = 'Entity Not Found'

    def __init__(self, entity_name, entity_id):
        super().__init__()
        self.entity_name = entity_name
        self.entity_id = entity_id

    def __str__(self):
        return f'{self.code} {self.name}: {self.entity_name} #{self.entity_id}'

    @property
    def description(self):
        return f'{self.entity_name} #{self.entity_id} does not exist or has been deleted.'


@exceptions.app_errorhandler(HTTPException)
def handle_http_exception(e):
    return render_template('http-exception.html', status=f'{e.code} {e.name}', description=e.description), e.code


@exceptions.app_errorhandler(EntityNotFound)
def handle_entity_not_found(e):
    return handle_http_exception(e)
