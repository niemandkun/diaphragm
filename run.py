#!/usr/bin/env python3

from diaphragm import application, database

#database.drop_all()
database.create_all()
application.run('127.0.0.1', 8080)
