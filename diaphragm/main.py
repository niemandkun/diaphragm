#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__, static_folder="static")

@app.route("/")
@app.route("/index.html")
def index():
    return "Hello from Flask!"

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
