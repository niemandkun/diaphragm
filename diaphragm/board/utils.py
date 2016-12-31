import re

from bleach import clean
from flask import make_response
from flask import render_template
from markupsafe import Markup


GREEN_TEXT = re.compile(r'(?<!>)(?<!<b)(?<!<i)(?<!<spoiler)>[^>][^\n]+')
CITE = re.compile(r'(?<!<b)(?<!<i)(?<!<spoiler)>>\d+')


def boardify(text):

    for green_text in GREEN_TEXT.findall(text):
        escaped = green_text.replace('>', '&gt', 1)
        tag = '<green>{}</green>'.format(escaped)
        text = text.replace(green_text, tag, 1)

    for cite in CITE.findall(text):
        escaped = cite.replace('>>', '&gt;&gt;', 1)
        tag = '<a href="#{}">{}</a>'.format(cite.replace('>>', '', 1), escaped)
        text = text.replace(cite, tag, 1)

    text = text.replace('\n', '<br/>')
    return Markup(clean(text, tags=['b', 'i', 'br', 'spoiler', 'green', 'a']))


def send_xml(threads, filename):
    xml = render_template("xml-template.html", threads=threads)

    response = make_response(xml)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)

    return response