from flask import Blueprint

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def home():
    """
    Endpoint just returns a welcome message.
    This is to demonstrate, how we can add endpoints across
    multiple files.
    """
    return 'Welcome to Atlassian Message Parser'
