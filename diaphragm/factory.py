import re
from flask import Flask
from bleach import clean
from markupsafe import Markup

GREEN_TEXT = re.compile(r'(?<!>)(?<!<b)(?<!<i)(?<!<spoiler)>[^>][^\n]+')
CITE = re.compile(r'(?<!<b)(?<!<i)(?<!<spoiler)>>\d+')


def do_clean(text):

    for green_text in GREEN_TEXT.findall(text):
        escaped = green_text.replace('>', '&gt', 1)
        tag = '<green>{}</green>'.format(escaped)
        text = text.replace(green_text, tag, 1)

    for cite in CITE.findall(text):
        escaped = cite.replace('>>', '&gt;&gt;', 1)
        tag = '<a href="#{}">{}</a>'.format(cite.replace('>>', '', 1), escaped)
        text = text.replace(cite, tag, 1)

    text = text.replace('\n', '<br/>')
    return Markup(clean(text, tags=['b', 'i', 'br', 'spoiler', 'green', 'a']))


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
