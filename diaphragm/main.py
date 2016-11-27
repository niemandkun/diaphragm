import os
import json

from flask import Flask
from flask import render_template, url_for, abort


app = Flask(__name__, static_folder="static")
app.config.from_object('diaphragm.config.ProductionConfig')


def render_ajax(*args, **kwargs):
    kwargs['dumps'] = json.dumps
    kwargs['standalone'] = True
    return render_template(*args, **kwargs)


@app.route("/")
@app.route("/<address>")
@app.route("/gallery/<address>")
def root(address=None):
    return render_template("layout.html")


@app.route("/api/")
def welcome():
    return render_ajax("welcome.html")


@app.route("/api/about")
def about():
    return render_ajax("about.html")


@app.route("/api/gallery")
def gallery():
    pictures = os.listdir(os.path.join(app.static_folder, 'gallery'))
    pictures = [os.path.join('gallery', x) for x in pictures]
    return render_ajax("gallery.html", full_size=None, pictures=pictures)


@app.route("/api/gallery/<filename>")
def get_image(filename):
    full_size = os.path.join('gallery', filename)
    if not os.path.isfile(os.path.join(app.static_folder, full_size)):
        abort(404)

    pictures = os.listdir(os.path.join(app.static_folder, 'gallery'))
    pictures = [os.path.join('gallery', x) for x in pictures]

    return render_ajax("gallery.html", full_size=full_size, pictures=pictures)


@app.route("/api/blog")
def blog():
    return render_ajax("coming_soon.html")


@app.route("/api/projects")
def projects():
    return render_ajax("projects.html")
