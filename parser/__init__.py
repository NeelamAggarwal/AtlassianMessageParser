import os
from flask import Flask
from config import config
from flask_injector import FlaskInjector
from injector import inject, singleton
from parser.helper.mentions import Mentions
from parser.helper.emoticons import Emoticons
from parser.helper.links import Links


def configureDefault(binder):
    """
    Binds objects which need to be independent for Testing
    """
    binder.bind(
        Mentions,
        to=Mentions(),
        scope=singleton,
    )
    binder.bind(
        Emoticons,
        to=Emoticons(),
        scope=singleton,
    )
    binder.bind(
        Links,
        to=Links(),
        scope=singleton,
    )


def create_app(configure=configureDefault, config_name=None):
    """
    create app object, loads configs for app
    and register for routes

    Params:
    config_name(str): 'either development or testing'

    Return:
    Flask object app
    """

    if config_name is None:
        config_name = os.environ.get('MESSAGE_PARSER_CONFIG', 'development')

    # creates the application object of class Flask
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # Divided app into different blueprints based on areas of functionality
    # Each blueprint will have its own routes.py file for routing
    from parser.api.route import api_blueprint
    from parser.main.route import main_blueprint

    # Register web application routes
    app.register_blueprint(main.route.main_blueprint)

    # Register API routes
    app.register_blueprint(api.route.api_blueprint, url_prefix='/api/v1')
    FlaskInjector(app=app, modules=[configure])
    return app
