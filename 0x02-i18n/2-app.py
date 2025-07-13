#!/usr/bin/env python3
"""
Create a get_locale function with the babel.localeselector decorator.
Use request.accept_languages
to determine the best match with our supported languages.
"""
from flask import Flask, render_template, request
from flask_babel import Babel

class Config():
    """ config class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/", strict_slashes=False)
def root():
    return render_template("2-index.html")

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run()
