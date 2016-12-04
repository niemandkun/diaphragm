from flask import render_template, abort, Blueprint, redirect

from diaphragm.utils import render_ajax

root = Blueprint("root", __name__,
                 static_folder="static",
                 static_url_path="/static/root",
                 template_folder="templates")


@root.route('/')
@root.route('/index')
def site_root():
    return redirect('/about')


@root.route('/<path:path>')
def any_page(path=None):
    return render_template("welcome.html")


@root.route("/api/")
def api_root():
    return render_ajax("welcome.html")


@root.route("/api/<path:path>")
def api_not_found(path):
    abort(404)
