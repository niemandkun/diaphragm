#!/usr/bin/env python3

from flask import Flask, render_template


app = Flask(__name__, static_folder="static")
app.config.from_object('config.DebugConfig')


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("layout.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
