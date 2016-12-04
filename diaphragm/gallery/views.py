from flask import abort, Blueprint

from diaphragm.gallery.models import Gallery
from diaphragm.utils import render_ajax, thumbnail, relative

gallery = Blueprint("gallery", __name__,
                    static_folder='static',
                    static_url_path='/static/gallery',
                    template_folder='templates')

images = Gallery(gallery.static_folder)


@gallery.route("/api/gallery")
def show_gallery():
    pictures = [relative(gallery.static_folder, thumbnail(x)) for x in images.list()]
    return render_ajax("gallery.html", full_size=None, pictures=pictures)


@gallery.route("/api/gallery/<filename>")
def get_image(filename):
    file_send = images.get(filename)

    if not file_send:
        abort(404)

    file_send = relative(gallery.static_folder, file_send)
    pictures = [relative(gallery.static_folder, thumbnail(x)) for x in images.list()]
    return render_ajax("gallery.html", full_size=file_send, pictures=pictures)
