import requests
import json
import os
import base64
from requests.auth import HTTPBasicAuth
from pprint import pprint


url = 'https://rational-club.kontrast-dev.com'
username, password, scope = (os.environ.get(i) for i in ['stage_user', 'stage_password', 'stage_scope'])

with requests.Session() as sess:
    payload = {'username': username,
               'password': password
    }
    r = requests.Request('POST', url+'/member/loginCC', data=payload)
    prepped = sess.prepare_request(r)
    print('request to:')
    print(prepped.url)
    print('-------------------------')
    print('request headers:')
    pprint(prepped.headers)
    print('-------------------------')
    print('request body:')
    pprint(prepped.body)
    print('-------------------------')
    response = sess.send(prepped)
    token = response.json().get('data')
    print('token retrieval success: {success}'.format(success=True if response.status_code==200 else False))
    print('-------------------------')

client_id, client_secret = (os.environ.get(i) for i in ['stage_client_id', 'stage_client_secret'])
token_url = 'https://www.connectedcooking.com/oauth/token'

with requests.Session() as token_sess:
    token_sess.headers.update({'scope': scope})
    payload = {'jwe': token,
               'grant_type': 'jwe_token',
               'client_secret': client_secret,
               'client_id': client_id}
    r = requests.Request('POST', token_url, auth=HTTPBasicAuth(client_id, client_secret), data=payload)
    prepped = token_sess.prepare_request(r)
    print('request to:')
    print(prepped.url)
    print('-------------------------')
    print('request headers:')
    pprint(prepped.headers)
    print('-------------------------')
    print('request body:')
    pprint(prepped.body)
    response = token_sess.send(prepped)
    print('token authentication success: {success}'.format(success=True if response.status_code==200 else False))
    print('-------------------------')
    print(response.status_code)
    print(response.json())
