from os import path, listdir
from datetime import datetime
from subprocess import call

IMAGES_EXT = {'png', 'jpg', 'jpeg', 'gif'}


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in IMAGES_EXT


def milliseconds(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds() * 1000)


def save(uploads_folder, thumbnail_folder, filename, data):
    _, ext = path.splitext(filename)
    filename = str(milliseconds(datetime.utcnow())) + ext

    upload_name = path.join(uploads_folder, filename)
    thumbnail_name = path.join(thumbnail_folder, filename)

    data.save(upload_name)
    create_thumbnail(upload_name, thumbnail_name)

    return filename


def create_thumbnail(original_path, thumbnail_path, size=128):
    command = [
        "convert",
        original_path,
        "-thumbnail",
        "{0}x{0}".format(size),
        thumbnail_path,
    ]
    print(command)
    call(command)


def create_thumbnails(images, static_folder, folder):
    thumb = Gallery(static_folder, folder)

    for image in images:
        thumb_path = path.join(thumb.abspath, path.basename(image))
        create_thumbnail(image, thumb_path)

    return thumb


class Gallery:
    def __init__(self, static_folder, folder, thumbnails=None):
        self.folder = folder
        self.thumbnails = thumbnails
        self.abspath = path.join(static_folder, folder)

    def list(self):
        images = listdir(self.abspath)
        return [path.join(self.folder, x) for x in images]

    def list_static(self):
        images = listdir(self.abspath)
        return [path.join(self.abspath, x) for x in images]

    def get(self, filename):
        full_path = path.join(self.abspath, filename)
        return path.join(self.folder, filename)\
            if self.__is_exist(full_path) else None

    def __is_exist(self, filepath):
        return path.isfile(filepath)
