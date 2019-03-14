import json
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from pprint import pprint


class Token:
    def __init__(self,
                 scope=os.environ.get('stage_scope'),
                 created=datetime.now(),
                 expires_in=86400,
                 valid=None,
                 details=None,
                 site='live',
                 token=None):
        self.scope = scope
        self.created = created
        self.expires_in = expires_in
        self.valid = valid
        self.details = details
        self.site = site
        self.token = token

    def check(self):
        if self.created + timedelta(seconds=self.expires_in) < datetime.now():
            self.valid = True
        else:
            self.valid = False
        return self.valid

    @classmethod
    def jwe(cls):
        return cls(expires_in=999999,
                   valid=True)


class JWEToken(Token):
    def import_local(self,
                     path=None):
        if path is None:
            path = self.site + '_jwe_token.json'
        try:
            with open(path) as fh:
                local = json.load(fh)
            self.token = local['jwe']
            self.details = local['details']
            self.created = datetime.now()
            self.valid = True
            return True
        except FileNotFoundError:
            self.valid = False
            return False

    def request(self, *,
                username: str = os.environ.get('live_user'),
                password: str = os.environ.get('live_password'),
                scope=None,
                url: str = 'https://www.club-rational.com/member/loginCC'):
        if scope is None:
            scope = self.scope
        payload = {'username': username,
                   'password': password}
        with requests.Session() as sess:
            sess.headers.update({'scope': scope})
            r = requests.Request('POST',
                                 url=url,
                                 data=payload)
            prepped = sess.prepare_request(r)
            response = sess.send(prepped)
            r_json = response.json()
        self.token = r_json.get('data')
        self.details = {'request_headers': dict(prepped.headers),
                        'request_body': prepped.body,
                        'request_url': prepped.url,
                        'response': response.status_code}
        result = True if self.details['response'] == 200 else False
        return result

    def export_local(self, path=None):
        if path is None:
            path = self.scope + '_jwe_token.json'
        data = {'jwe': self.token,
                'details': self.details}
        with open(path, mode='w') as fh:
            json.dump(data, fh)


class BearerToken(Token):
    def __init__(self,
                 refresh_token=None,
                 valid_to=None):
        super().__init__()
        self.refresh_token = refresh_token
        self.valid_to = valid_to

    def import_local(self,
                     path=None):
        if path is None:
            path = self.site + '_bearer_token.json'
        try:
            with open(path) as fh:
                local = json.load(fh)
                self.token = local['token']
                self.details = local['details']
                self.refresh_token = local['refresh_token']
                self.valid_to = datetime.strptime(local['valid_to'], '%Y-%m-%d %H:%M:%S.%f')
            return True
        except FileNotFoundError:
            self.valid = False
            return False

    def export_local(self,
                     path=None):
        if path is None:
            path = self.site + '_bearer_joken.json'
        data = {'token': self.token,
                'details': self.details,
                'valid_to': str(self.valid_to),
                'refresh_token': self.refresh_token}
        try:
            with open(path, mode='w') as fh:
                json.dump(data, fh)
            return True
        except FileNotFoundError:
            return False

    def request(self,
                jwe: str,
                client_id: str = os.environ.get('live_client_id'),
                client_secret: str = os.environ.get('live_client_secret'),
                scope: str = os.environ.get('stage_scope'),
                url: str = 'https://www.connectedcooking.com/oauth/token'):
        payload = {'jwe': jwe,
                   'grant_type': 'jwe_token'}
        with requests.Session() as sess:
            sess.headers.update({'scope': scope})
            r = requests.Request(method='POST',
                                 url=url,
                                 data=payload,
                                 auth=HTTPBasicAuth(client_id, client_secret))
            prepped = sess.prepare_request(r)
            response = sess.send(prepped)
            r_json = response.json()
        self.token = r_json.get('access_token')
        self.refresh_token = r_json.get('refresh_token')
        self.valid_to = datetime.now() + timedelta(seconds=int(r_json.get('expires_in')))
        self.valid = False if r_json.get('access_token') is None else True
        self.site = url
        self.details = {'request_headers': dict(prepped.headers),
                        'request_url': prepped.url,
                        'request_body': prepped.body,
                        'response': response.status_code}
        return True if self.details['response'] == 200 else False


# to do: shift check function downstream to BearerToken
# to do: test JWE/Bearer local import/export
# add refresh function to both


if __name__ == '__main__':
    jwe_test = JWEToken()
    print(jwe_test.valid)
    print(jwe_test.expires_in)
    print(jwe_test.scope)
    print(jwe_test.site)
    print(jwe_test.check())
#    print(jwe_test.import_local())
    pprint(jwe_test.import_local())


