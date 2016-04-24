import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import base64
import json
import requests
import urllib

from bottle import request, route, run, template
from ringcentral import SDK

myState = 'myState'
token_json = '{}'

rcsdk = SDK(os.environ.get('RC_APP_KEY'), os.environ.get('RC_APP_SECRET'), os.environ.get('RC_APP_SERVER_URL'))

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
    auth_uri = authorize_uri({'state': myState})
    redirect_uri = os.environ.get('RC_APP_REDIRECT_URL')
    token = rcsdk.platform().auth().data()
    token_json = ''
    if token['access_token']:
        token_json = json.dumps(token, sort_keys=True,
            indent=4, separators=(',', ': '))

    return template('index', authorize_uri=auth_uri, redirect_uri=redirect_uri, token_json=token_json)

@route('/callback')
def callback():
    auth_code = request.params['code']
    token_json = get_access_token(auth_code)
    rcsdk.platform().auth().set_data(json.loads(token_json))
    return template('index', authorize_uri='', redirect_uri='', token_json=token_json)

run(host=os.environ.get('MY_APP_HOST'), port=os.environ.get('MY_APP_PORT'), debug=True)
