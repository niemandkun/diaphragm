import json
from datetime import datetime
from os import path, makedirs
from subprocess import call

from PIL import Image
from flask import render_template
from werkzeug.utils import secure_filename

IMAGES_EXT = {'png', 'jpg', 'jpeg', 'gif'}


def pluralize(singular, count):
    if count > 1:
        if singular.endswith("y"):
            return singular[:-1] + "ies"
        return singular + "s"
    return singular


def json_dict(**kwargs):
    return json.dumps(kwargs)


def render_ajax(*args, **kwargs):
    kwargs['dumps'] = json.dumps
    kwargs['standalone'] = True
    return render_template(*args, **kwargs)


def relative(static_folder, path_to_file):
    return path.relpath(path_to_file, static_folder)


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in IMAGES_EXT


def milliseconds(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds() * 1000)


def safely_upload(uploads_folder, data):
    original_filename = secure_filename(data.filename)

    if not is_allowed_file(original_filename):
        return None

    _, ext = path.splitext(original_filename)
    filename = str(milliseconds(datetime.utcnow())) + ext
    upload_name = path.join(uploads_folder, filename)
    data.save(upload_name)
    create_thumbnail(upload_name)
    return filename


def create_thumbnail(original_path, size=(128,128)):
    thumbnail_path = thumbnail(original_path)
    thumbnail_folder = path.dirname(thumbnail_path)

    if not path.exists(thumbnail_folder):
        makedirs(thumbnail_folder)

    im = Image.open(original_path)
    im.thumbnail(size)
    im.save(thumbnail_path)


def create_thumbnails(images):
    for image in images:
        create_thumbnail(image)


def thumbnail(original_path):
    filename = path.basename(original_path)
    dirname = path.dirname(original_path)
    return path.join(dirname, "thumbnails", filename)
