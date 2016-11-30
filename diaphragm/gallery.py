import os
from subprocess import call


def create_thumbnails(images, static_folder, folder):
    thumb = Gallery(static_folder, folder)

    for image in images:
        thumb_path = os.path.join(thumb.abspath, os.path.basename(image))
        create_thumbnail(image, thumb_path)

    return thumb


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


class Gallery:
    def __init__(self, static_folder, folder):
        self.folder = folder
        self.abspath = os.path.join(static_folder, folder)

    def list(self):
        images = os.listdir(self.abspath)
        return [os.path.join(self.folder, x) for x in images]

    def list_static(self):
        images = os.listdir(self.abspath)
        return [os.path.join(self.abspath, x) for x in images]

    def get(self, filename):
        full_path = os.path.join(self.abspath, filename)
        return full_path if self.__is_exist(full_path) else None

    def __is_exist(self, filepath):
        return os.path.isfile(filepath)
