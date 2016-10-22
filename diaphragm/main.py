#!/usr/bin/env python3

from flask import Flask, render_template


app = Flask(__name__, static_folder="static")
app.config.from_object('config.DebugConfig')


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("layout.html")

# @app.route("/blog")
# def blog():
#     return "<div>blog</div>"

@app.route("/projects")
def projects():
    from time import sleep
    sleep(2)
    return "<div>projects</div>"

@app.route("/about")
def about():
    return "<div>about</div>"

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
