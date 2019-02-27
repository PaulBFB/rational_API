import requests
import os
import datetime
from requests.auth import HTTPBasicAuth
from pprint import pprint


logon_url = 'https://rational-club.kontrast-dev.com/member/loginCC'
token_url = 'https://stage.connectedcooking.com/oauth/token'


def login_stage(*,
                username=os.environ.get('stage_user'),
                password=os.environ.get('stage_password'),
                scope=os.environ.get('stage_scope')):
    payload = {'username': username,
               'password': password}
    with requests.Session() as sess:
        sess.headers.update({'scope': scope})
        r = requests.Request('POST', url=logon_url, data=payload)
        prepped = sess.prepare_request(r)
        response = sess.send(prepped)
        token = response.json().get('data')
    return {'response': response.status_code,
            'jwe': token,
            'details': {'request_headers': prepped.headers,
                        'request_body': prepped.body}}


def get_bearer(*,
               jwe=login_stage().get('jwe'),
               client_id=os.environ.get('stage_client_id'),
               client_secret=os.environ.get('stage_client_secret')):
    payload = {'jwe': jwe,
               'client_id': client_id,
               'client_secret': client_secret,
               'grant_type': 'jwe_token'}
    with requests.Session() as sess:
        r = requests.Request('POST', url=token_url, auth=HTTPBasicAuth(username=client_id, password=client_secret), data=payload)
        prepped = sess.prepare_request(r)
        response = sess.send(prepped)
    return {'response': response.status_code,
            'token': response.json().get('access_token'),
            'expires_in': response.json().get('expires_in'),
            'refresh_token': response.json().get('refresh_token'),
            'details': {'request_headers': prepped.headers,
                        'request_body': prepped.body,
                        'token_type': response.json().get('token_type'),
                        'scope': response.json().get('scope')}}


if __name__ == '__main__':
    print('testing function - login:')
    pprint(login_stage().get('response'))
    print('----------------------------')
    print('testing function - token')
    pprint(get_bearer().get('response'))
    print('token received is valid until: {expiration}'.format(expiration=datetime.datetime.now() +
                                                                          datetime.timedelta(seconds=int(get_bearer().get('expires_in')))))
