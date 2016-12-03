import json

from flask import render_template


def json_dict(**kwargs):
    return json.dumps(kwargs)


def render_ajax(*args, **kwargs):
    kwargs['dumps'] = json.dumps
    kwargs['standalone'] = True
    return render_template(*args, **kwargs)
