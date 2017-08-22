import os

"""
Configuration for the application.
An application should have different configuration
for different environments (Eg: Development, Testing, Staging and Production).

This is used to initialize the application based on the
environment variable 'MESSAGE_PARSER_CONFIG' in create_app.
"""


class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class StagingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
