class Config:
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True
    THUMBNAILS_FOLDER = "thumbnails"
    GALLERY_FOLDER = "gallery"
    UPLOADS_FOLDER = "uploads"


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SECRET_KEY = "secret"
