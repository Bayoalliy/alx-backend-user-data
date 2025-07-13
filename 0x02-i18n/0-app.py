#!/usr/bin/env python3
"""
setup a basic Flask app in 0-app.py . Create a single / route
"""
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def root():
    return render_template("0-index.html")

if __name__ == '__main__':
    app.run()
