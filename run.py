import sys
import subprocess
from flask_script import Manager
from parser import create_app
from flask_injector import FlaskInjector
from injector import inject, singleton
from parser.helper.mentions import Mentions
from parser.helper.emoticons import Emoticons
from parser.helper.links import Links

"""
Script that starts up the development web server for our application
"""

# manager instance to receive input from the command line.
manager = Manager(create_app())


@manager.command
def test():
    """
    Runs Unit Tests
    """
    tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
    sys.exit(tests)


if __name__ == '__main__':
    """
    Starts the flask server
    After the server initializes it will listen on port 5000(default) waiting for requests
    """
    manager.run()
