import re
from flask import Flask
from bleach import clean
from markupsafe import Markup


GREEN_TEXT = re.compile(r'\>[^\n]*\n')


def do_clean(text):
    for green_text in GREEN_TEXT.findall(text):
        print(green_text)
        text = text.replace(green_text, '<green>{}</green>'.format(green_text))

    text = text.replace('\n', '<br/>')
    return Markup(clean(text, tags=['b', 'i', 'br', 'spoiler', 'green']))


def create_app(config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config)
    app.jinja_env.filters['clean'] = do_clean

    from diaphragm.about.views import about
    app.register_blueprint(about)

    from diaphragm.root.views import root
    app.register_blueprint(root)

    from diaphragm.gallery.views import gallery
    app.register_blueprint(gallery)

    from diaphragm.board.views import board
    app.register_blueprint(board)

    from diaphragm.counter.views import counter
    app.register_blueprint(counter)

    from diaphragm.database import db
    db.app = app
    db.init_app(app)
    app.db = db

    return app
