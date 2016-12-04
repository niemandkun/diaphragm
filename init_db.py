#!/usr/bin/env python3

from diaphragm import application

application.db.drop_all()
application.db.create_all()
