from flask import Flask, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth, OAuthException
from secret_keys import fb_id, fb_secret

# Create the app and configuration
# Read the configuration file
app = Flask(__name__)
app.config.from_object('application.default_settings')
app.config.from_envvar('PRODUCTION_SETTINGS', silent=True)

FACEBOOK_APP_ID = fb_id
FACEBOOK_APP_SECRET = fb_secret
oauth = OAuth(app)
facebook = oauth.remote_app(
            'facebook',
            consumer_key=FACEBOOK_APP_ID,
            consumer_secret=FACEBOOK_APP_SECRET,
            request_token_params={'scope': 'email'},
            base_url='https://graph.facebook.com',
            request_token_url=None,
            access_token_url='/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth'
)


# Connect to database with sqlalchemy.
db = SQLAlchemy(app)


# 404 page not found "route"
@app.errorhandler(404)
def not_found(error):
    title = "404 Page not found"
    return render_template('404.html', title=title), 404


# 500 server error "route"
@app.errorhandler(500)
def server_error(error):
    title = "500 Server Error"
    db.session.rollback()
    return render_template('500.html', title=title), 500


import application.manager
