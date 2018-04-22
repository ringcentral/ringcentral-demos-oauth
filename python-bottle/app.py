import base64
from dotenv import load_dotenv
import json
import os
from os.path import join, dirname
import requests
import urllib

env_path = os.environ['ENV_PATH']

if not env_path:
    env_path = join(dirname(__file__), '.env')

load_dotenv(env_path)

from bottle import request, route, run, template
from ringcentral import SDK

myState = 'myState'
token_json = '{}'

rcsdk = SDK(
    os.environ.get('RINGCENTRAL_CLIENT_ID'),
    os.environ.get('RINGCENTRAL_CLIENT_SECRET'),
    os.environ.get('RINGCENTRAL_SERVER_URL'))

def authorize_uri(options):
    base_url = os.environ.get('RINGCENTRAL_SERVER_URL') + '/restapi/oauth/authorize'
    params = (
        ('response_type', 'code'),
        ('redirect_uri', os.environ.get('RINGCENTRAL_REDIRECT_URL')),
        ('client_id', os.environ.get('RINGCENTRAL_CLIENT_ID')),
        ('state', options['state'])
    )
    qs = urllib.urlencode(params)
    auth_url = base_url + '?' + qs
    return auth_url

def get_access_token(auth_code):
    token_url = os.environ.get('RINGCENTRAL_SERVER_URL') + '/restapi/oauth/token'

    values = {'grant_type' : 'authorization_code',
        'code' : auth_code,
        'redirect_uri' : os.environ.get('RINGCENTRAL_REDIRECT_URL') }
    data = urllib.urlencode(values)

    api_key = os.environ.get('RINGCENTRAL_CLIENT_ID') + ':' + os.environ.get('RINGCENTRAL_CLIENT_SECRET')
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
    redirect_uri = os.environ.get('RINGCENTRAL_REDIRECT_URL')
    token = rcsdk.platform().auth().data()
    token_json = ''
    if token['access_token']:
        token_json = json.dumps(token, sort_keys=True,
            indent=4, separators=(',', ': '))

    return template('index', authorize_uri=auth_uri, redirect_uri=redirect_uri, token_json=token_json)

@route('/oauth2callback')
def callback():
    auth_code = request.params['code']
    token_json = get_access_token(auth_code)
    rcsdk.platform().auth().set_data(json.loads(token_json))
    return template('index', authorize_uri='', redirect_uri='', token_json=token_json)

run(host=os.environ.get('MY_APP_HOST'), port=os.environ.get('MY_APP_PORT'), debug=True)
