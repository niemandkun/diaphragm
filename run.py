#!/usr/bin/env python3

from diaphragm import create_app


app = create_app('diaphragm.config.DebugConfig')
app.run('0.0.0.0', 8080)
