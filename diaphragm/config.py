class Config:
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''
    DEBUG = False


class DebugConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SECRET_KEY = "secret"
    DEBUG = True
