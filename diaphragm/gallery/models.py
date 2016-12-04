from os import path, listdir

from diaphragm.utils import create_thumbnails


class Gallery:
    def __init__(self, gallery_folder):
        self.abspath = gallery_folder
        create_thumbnails(self.list())

    def list(self):
        images = [path.join(self.abspath, p) for p in listdir(self.abspath)]
        return [p for p in images if path.isfile(p)]

    def get(self, filename):
        fullpath = path.join(self.abspath, filename)
        return fullpath if path.isfile(fullpath) else None
