#!/usr/bin/env python3
"""
Create a get_locale function with the babel.localeselector decorator.
Use request.accept_languages
to determine the best match with our supported languages.
"""
from flask import Flask, render_template, request, g
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

users = {
 1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
 2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
 3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
 4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
 }

def get_user(id):
    if not id:
        return None
    return users.get(id)

@app.before_request
def before_request():
    u_id =  request.args.get('login_as')
    g.user = get_user(int(u_id))

@app.route("/", strict_slashes=False)
def root():
    return render_template("5-index.html", user=g.user)

@babel.localeselector
def get_locale():
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run()
