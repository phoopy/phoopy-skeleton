from phoopy.http.annotations import route, errorhandler
from .abstract_controller import AbstractController
from flask import render_template
from .middleware import app_header


class MainController(AbstractController):
    def __init__(self, kernel):
        super(MainController, self).__init__(kernel)

    @route('GET', '/', 'index')
    @app_header()
    def index(self, time):
        return render_template('main/index.html')

    @route('GET', '/main-api/<name>', 'main_api')
    @app_header()
    def main_api(self, name, time):
        return self.create_item_response({
            'message': 'Hello {}'.format(name)
        })

    @errorhandler(Exception)
    @app_header()
    def error(self, error, time):
        return self.create_error_response(
            999,
            error.description if hasattr(error, 'description') else str(error),
            error.code if hasattr(error, 'code') else 500
        )
