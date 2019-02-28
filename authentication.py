import json
import requests
import os
import datetime as dt
from requests.auth import HTTPBasicAuth
from pprint import pprint


logon_url = 'https://rational-club.kontrast-dev.com/member/loginCC'
token_url = 'https://stage.connectedcooking.com/oauth/token'


def login_stage(*,
                username: str = os.environ.get('stage_user'),
                password: str = os.environ.get('stage_password'),
                scope: str = os.environ.get('stage_scope')) -> dict:
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
            'details': {'request_headers': dict(prepped.headers),
                        # header object needs to be converted to dict to be JSON serializable
                        'request_body': prepped.body}}


def get_bearer(*,
               jwe: str = login_stage().get('jwe'),
               client_id: str = os.environ.get('stage_client_id'),
               client_secret: str = os.environ.get('stage_client_secret')) -> dict:
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
            'details': {'request_headers': dict(prepped.headers),
                        # header object needs to be converted to dict to be JSON serializable
                        'request_body': prepped.body,
                        'token_type': response.json().get('token_type'),
                        'scope': response.json().get('scope')}}


if __name__ == '__main__':
    print('testing function - login:')
    pprint(login_stage().get('response'))
    print('----------------------------')
    print('testing function - token')
    bearer = get_bearer()
    # datetime needs to be converted to string to dump into JSON (datetime is not JSON serializable)
    bearer['valid_to'] = str(dt.datetime.now() + dt.timedelta(seconds=bearer.get('expires_in')))
    pprint(bearer.get('response'))
    print('token received is valid until: {expiration}'.format(expiration=dt.datetime.now() +
                                                                          dt.timedelta(seconds=int(get_bearer().get('expires_in')))))
    print('----------------------------')
    print('saving data to current directory as json')
    with open('token.json', mode='w') as fh:
        json.dump(bearer, fh)
    print('authentication successfully written to current directory')
