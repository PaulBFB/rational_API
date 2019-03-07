import json
import requests
import os
import datetime as dt
from requests.auth import HTTPBasicAuth
from pprint import pprint


logon_url_stage = 'https://rational-club.kontrast-dev.com/member/loginCC'
logon_url_live = 'https://www.club-rational.com/member/loginCC'
token_url_stage = 'https://stage.connectedcooking.com/oauth/token'
token_url_live = 'https://www.connectedcooking.com/oauth/token'


def cc_login(*,
             username: str = os.environ.get('stage_user'),
             password: str = os.environ.get('stage_password'),
             scope: str = os.environ.get('stage_scope'),
             url: str = 'https://rational-club.kontrast-dev.com/member/loginCC') -> dict:
    payload = {'username': username,
               'password': password}
    with requests.Session() as sess:
        sess.headers.update({'scope': scope})
        r = requests.Request('POST',
                             url=url,
                             data=payload)
        prepped = sess.prepare_request(r)
        response = sess.send(prepped)
        token = response.json().get('data')
    return {'response': response.status_code,
            'jwe': token,
            'details': {'request_headers': dict(prepped.headers),
                        # header object needs to be converted to dict to be JSON serializable
                        'request_body': prepped.body,
                        'request_url': url}}


# needs check - token present & up to date --> don't refresh!
def get_bearer(*,
               jwe: str = cc_login().get('jwe'),
               client_id: str = os.environ.get('stage_client_id'),
               client_secret: str = os.environ.get('stage_client_secret'),
               scope: str = os.environ.get('stage_scope'),
               url: str = 'https://stage.connectedcooking.com/oauth/token') -> dict:
    payload = {'jwe': jwe,
               'client_id': client_id,
               'client_secret': client_secret,
               'grant_type': 'jwe_token'}
    with requests.Session() as sess:
        sess.headers.update({'scope': scope})
        r = requests.Request('POST',
                             url=url,
                             auth=HTTPBasicAuth(username=client_id, password=client_secret),
                             data=payload)
        prepped = sess.prepare_request(r)
        response = sess.send(prepped)
    return {'response': response.status_code,
            'token': response.json().get('access_token'),
            'expires_in': response.json().get('expires_in'),
            'refresh_token': response.json().get('refresh_token'),
            'details': {'request_headers': dict(prepped.headers),
                        # header object needs to be converted to dict to be JSON serializable
                        'request_body': prepped.body,
                        'request_url': url,
                        'token_type': response.json().get('token_type'),
                        'scope': response.json().get('scope')}}


if __name__ == '__main__':
    t_o_l = 'l'
    # input('test live or stage? - l/s: ')
    login_test, url, user, password = None, None, None, None
    if t_o_l not in ['s', 'l']:
        print('invalid choice')
        quit()
    elif t_o_l == 's':
        print('testing function - login(stage):')
        url = logon_url_stage
        user = os.environ.get('stage_user')
        password = os.environ.get('stage_password')
    else:
        print('testing function - login(live):')
        url = logon_url_live
        user = os.environ['live_user']
        password = os.environ['live_password']
    login_test = cc_login(url=url,
                          username=user,
                          password=password)
    print('user', user)
    print('password', password)
    pprint(login_test)
    print('----------------------------')
    print('testing function - token')
    if t_o_l == 's':
        bearer = get_bearer()
    else:
        bearer = get_bearer(url=token_url_live,
                            client_id=os.environ.get('live_client_id'),
                            client_secret=os.environ.get('live_client_secret'),
                            jwe=login_test.get('jwe'))
        pprint(bearer)
    # datetime needs to be converted to string to dump into JSON (datetime is not JSON serializable)
    if bearer.get('response') in [400, 404, 401]:
        print('authentication failed')
        quit()
    else:
        pass
    bearer['valid_to'] = str(dt.datetime.now() + dt.timedelta(seconds=bearer.get('expires_in')))
    pprint(bearer.get('response'))
    print('token received is valid until: {expiration}'.
          format(expiration=dt.datetime.now() + dt.timedelta(seconds=int(get_bearer().get('expires_in')))))
    print('----------------------------')
    print('saving data to current directory as json')
    with open('live_bearer_token.json', mode='w') as fh:
        json.dump(bearer, fh)
    print('authentication successfully written to current directory')
