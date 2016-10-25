import json

from flask import Flask
from flask import render_template


app = Flask(__name__, static_folder="static")
app.config.from_object('diaphragm.config.ProductionConfig')


def render_ajax(*args, **kwargs):
    kwargs['dumps'] = json.dumps
    kwargs['standalone'] = True
    return render_template(*args, **kwargs)


@app.route("/")
@app.route("/<address>")
def root(address=None):
    return render_template("layout.html")


@app.route("/api/")
def welcome():
    return render_ajax("welcome.html")


@app.route("/api/about")
def about():
    return render_ajax("about.html")


@app.route("/api/blog")
def blog():
    return render_ajax("coming_soon.html")


@app.route("/api/projects")
def projects():
    return render_ajax("coming_soon.html")
