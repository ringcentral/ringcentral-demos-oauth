import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from bottle import request, route, run, template

import base64
import requests
import urllib

myState = 'myState'
token_json = '{}'

def authorize_uri(options):
    base_url = os.environ.get('RC_APP_SERVER_URL') + '/restapi/oauth/authorize'
    params = (
        ('response_type', 'code'),
        ('redirect_uri', os.environ.get('RC_APP_REDIRECT_URL')),
        ('client_id', os.environ.get('RC_APP_KEY')),
        ('state', options['state'])
    )
    qs = urllib.urlencode(params)
    auth_url = base_url + '?' + qs
    return auth_url

def get_access_token(auth_code):
    token_url = os.environ.get('RC_APP_SERVER_URL') + '/restapi/oauth/token'
    values = {'grant_type' : 'authorization_code',
        'code' : auth_code,
        'redirect_uri' : os.environ.get('RC_APP_REDIRECT_URL') }
    data = urllib.urlencode(values)

    api_key = os.environ.get('RC_APP_KEY') + ':' + os.environ.get('RC_APP_SECRET')
    api_key = base64.b64encode(api_key)
    headers = {'Authorization': 'Basic ' + api_key,
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, data=data, headers=headers)
    json = response.text
    return json

@route('/')
def index():
    auth_uri = authorize_uri({
        'state': myState
    })
    redirect_uri = os.environ.get('RC_APP_REDIRECT_URL')

    return template('index', authorize_uri=auth_uri, redirect_uri=redirect_uri, token_json='')

@route('/callback')
def callback():
    auth_code = request.params['code']
    token_json = get_access_token(auth_code)
    return template('index', authorize_uri='', redirect_uri='', token_json=token_json)
    return auth_code

run(host=os.environ.get('MY_APP_HOST'), port=os.environ.get('MY_APP_PORT'), debug=True)
