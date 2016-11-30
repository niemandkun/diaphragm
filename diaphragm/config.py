class Config:
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True
    THUMBNAILS= "thumbnails"
    GALLERY = "gallery"


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False


class DebugConfig(Config):
    DEBUG = True
