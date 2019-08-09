# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify, render_template_string
from werkzeug.exceptions import *
from user_control import *

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='[[',
        variable_end_string=']]'
    ))


def create_app():
    """
    Create a flask app
    :return: flask app
    """
    app = CustomFlask(__name__)

    @app.after_request
    def add_header(r):
        r.headers['Cache-Control'] = 'public,max-age=0'
        return r

    app.secret_key = os.urandom(24)
    app.config.from_pyfile('config.py')
    configure_extensions(app)
    configure_blueprints(app)
    configure_log_handlers(app)
    configure_error_handlers(app)
    configure_main_route(app)

    return app


def configure_extensions(app):
    """
    Init app
    :param app: flask app
    :return: not return
    """


def configure_blueprints(app):
    """
    Registry flask url
    :param app: flask app
    :return: not return
    """
    app.register_blueprint(routes)



def configure_log_handlers(app):
    """
    Config log
    :param app: flask app
    :return: not return
    """



def configure_error_handlers(app):
    """
    Handle error process
    :param app: flask app
    :return: not return
    """

    @app.errorhandler(400)
    def bad_request(error):
        app.logger.info(error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 400
        else:
            return jsonify(error={'code': 400,
                                  'message': 'Bad Request.'}), 400

    @app.errorhandler(401)
    def unauthorized_request(error):
        app.logger.info(error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 401
        else:
            return jsonify(error={
                'code': 401,
                'message': 'Unauthorized Request.'}), 401

    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.info(error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 405
        else:
            return render_template_string('Page not Found'), 404

    @app.errorhandler(405)
    def request_not_found(error):
        app.logger.info(error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 405
        else:
            return jsonify(error={
                'code': 405,
                'message': 'The method is not allowed '
                           'for the requested URL.'}), 405

    @app.errorhandler(415)
    def request_not_support_type(error):
        app.logger.info(error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 415
        else:
            return jsonify(error={
                'code': 415,
                'message': 'The server does not support the media type '
                           'transmitted in the request.'}), 415

    @app.errorhandler(UnsupportedMediaType)
    def request_not_support_type_by_exception(error):
        app.logger.info(error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 415
        else:
            return jsonify(error={
                'code': 415,
                'message': 'The server does not support the media type '
                           'transmitted in the request.'}), 415

    @app.errorhandler(Exception)
    def default_exception(error):
        app.logger.info(error)
        if error.message != '':
            return jsonify(error={'code': 500,
                                  'message': error.message}), 500
        else:
            return jsonify(error={'code': 500,
                                  'message': 'Internal Error.'}), 500



def configure_main_route(app):
    """
    Config main url route of app
    :param app: flask app (main app)
    :return:
    """
	#
    # @app.route('/', methods=['GET', 'POST'])
    # def viettel_waf_captcha():
    #    return str(request.headers)
	