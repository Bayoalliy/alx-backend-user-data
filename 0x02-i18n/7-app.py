#!/usr/bin/env python3
"""
Create a get_locale function with the babel.localeselector decorator.
Use request.accept_languages
to determine the best match with our supported languages.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from datetime import datetime

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
    #Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    #Locale from user settings
    if g.user and  g.user['locale'] in app.config['LANGUAGES']):
        return g.user['locale']

    #Locale from request header
    if request.headers.get('locale') in app.config['LANGUAGES']):
        return request.headers.get('locale')

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    #timezone from URL parameters
    t_zone = request.args.get('timezone')
    if t_zone:
        try:
            user_pytz = pytz.timezone(t_zone)
            return t_zone
        except pytz.exceptions.UnknownTimeZoneError:
            return

    #timezone from user settings
    if g.user and  g.user['timezone']:
        try:
            user_pytz = pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == '__main__':
    app.run()
