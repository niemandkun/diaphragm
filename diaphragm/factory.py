from flask import Flask


def create_app(config):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config)

    from diaphragm.database import db
    db.app = app
    db.init_app(app)

    from diaphragm.about.views import about
    app.register_blueprint(about)

    from diaphragm.root.views import root
    app.register_blueprint(root)

    from diaphragm.gallery.views import gallery
    app.register_blueprint(gallery)

    from diaphragm.board.views import board
    app.register_blueprint(board)

    return app
