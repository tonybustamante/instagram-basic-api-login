"""
Module Name: instagram_basic_api.py
Author: Anthony Bustamante (anthony.bustamante@gmail.com)
Date: April 23, 2023
Description: This python program implements authentication for the Instagram Basic Diplay API found here: https://developers.facebook.com/docs/instagram-basic-display-api/getting-started
"""



import time
import secrets
import flask
import requests
import logging
from urllib.parse import urlencode 
import json
import os
import configparser


## SETUP ##
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%d/%m/%y %H:%M:%S"
)

## APP_ID and APP_SECRET can be found on the instagram basic app on the developers page. 
APP_ID = os.environ.get("IG_BASIC_APP_ID") 
APP_SECRET = os.environ.get("IG_BASIC_APP_SECRET") 

CALLBACK_URI = config['urls']['CALLBACK_URI']
DASHBOARD_URI= config['urls']['DASHBOARD_URI']

## Create the application.
app = flask.Flask(__name__)
app.secret_key = secrets.token_hex(16) + str(int(time.time()))


# Middleware function to check for authentication on every request
# TODO: auth and callback routes should not be accessible after login
@app.before_request
def require_authentication():
    if 'state' not in flask.session.keys(): 
        if flask.request.path != '/auth':
            return flask.redirect(flask.url_for('auth'))
    elif 'user_id' not in flask.session.keys():
        if flask.request.path != '/auth/callback':
            return flask.redirect(flask.url_for('auth_callback'))

@app.route('/auth')
def auth():
    state = secrets.token_hex(16) + str(int(time.time()))
    flask.session['state'] = state
    params = { 
        'client_id': APP_ID,
        'redirect_uri': CALLBACK_URI,
        'scope': 'user_profile,user_media',
        'response_type': 'code'
    }
    login_uri = 'https://api.instagram.com/oauth/authorize?' + urlencode(params)
    logging.info("Login URI: ", login_uri)
    return(flask.redirect(login_uri))

@app.route('/auth/callback')
def auth_callback():
    code = flask.request.args.get('code')
    token_byte_data = get_token(code)
    decoded_token = token_byte_data.content.decode('utf-8')
    token_data = json.loads(decoded_token)
    flask.session['access_token'] = token_data['access_token'] 
    flask.session['user_id'] = token_data['user_id'] 
    return(flask.redirect(flask.url_for('dashboard')))

def get_token(code):
    params = dict()
    params = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': CALLBACK_URI,
        'code': code
    }
    response = requests.post('https://api.instagram.com/oauth/access_token', data=params)
    return(response)    

def get_token_details(token):
    params = { 
        'input_token': token
    }
    url =  + '?' + 'access_token=' + APP_ID + '|' + APP_SECRET
    response = requests.post(url, params)
    return(response)


@app.route('/dashboard')
def dashboard():
    return('DASHBOARD!')

@app.route('/profile')
def profile():
    return('PROFILE!')

if __name__ == '__main__':
    app.debug=True
    app.run(ssl_context='adhoc')