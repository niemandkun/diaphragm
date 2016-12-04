import sys

activate_this = '/var/www/diaphragm/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.append('/var/www/diaphragm')

from diaphragm import application
