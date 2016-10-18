#!/usr/bin/env python2

from distutils.core import setup


setup(name='diaphragm',
      version='0.0-dev1',
      description="A web application brave enough to serve niemandkun's place.",
      author='niemandkun',
      author_email='niemandkun@yandex.ru',
      url='niemandkun.tech',
      packages=['diaphragm'],
      scripts=['bin/diaphragm.wsgi'],

      package_data={
        'diaphragm': [
            'diaphragm/static/',
            'diaphragm/templates/',
        ]
      },

      install_requires=[
        'click >= 6.6',
        'Flask >= 0.11.1',
        'itsdangerous >= 0.24',
        'Jinja2 >= 2.8',
        'MarkupSafe >= 0.23',
        'Werkzeug >= 0.11.11',
      ],
     )
