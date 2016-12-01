import os
import json

from flask import Flask
from flask import render_template, url_for, abort

from diaphragm.gallery import Gallery, create_thumbnails


app = Flask(__name__, static_folder="static")
app.config.from_object('diaphragm.config.ProductionConfig')

gallery = Gallery(app.static_folder, app.config["GALLERY"])
thumbnails = create_thumbnails(gallery.list_static(),
                               app.static_folder, app.config["THUMBNAILS"])


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
def show_gallery():
    pictures = thumbnails.list()
    return render_ajax("gallery.html", full_size=None, pictures=pictures)


@app.route("/api/gallery/<filename>")
def get_image(filename):
    file_send = gallery.get(filename)

    if not file_send:
        abort(404)

    pictures = thumbnails.list()
    return render_ajax("gallery.html", full_size=file_send, pictures=pictures)


@app.route("/api/blog")
def blog():
    return render_ajax("coming_soon.html")


@app.route("/api/projects")
def projects():
    return render_ajax("projects.html")
