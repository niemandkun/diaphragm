class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False
    DEBUG = False


class DebugConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SECRET_KEY = "secret"
    DEBUG = True
