from flask import Blueprint

from diaphragm.utils import render_ajax

about = Blueprint("about", __name__,
                  static_folder="static",
                  static_url_path="/static/about",
                  template_folder="templates")


@about.route("/api/about")
def about_page():
    return render_ajax("about.html")


@about.route("/api/blog")
def blog_page():
    return render_ajax("coming_soon.html")


@about.route("/api/projects")
def projects_page():
    return render_ajax("projects.html")
