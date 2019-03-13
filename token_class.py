import json
import os
import requests
from datetime import datetime, timedelta
from pprint import pprint
from time import sleep


class Token:
    def __init__(self,
                 scope=os.environ.get('stage_scope'),
                 created=datetime.now(),
                 expires_in=86400,
                 valid=None):
        self.scope = scope
        self.created = created
        self.expires_in = expires_in
        self.valid = valid

    def check(self):
        if self.created + timedelta(seconds=self.expires_in) > datetime.now():
            self.valid = True
        else:
            self.valid = False
        return self.valid


class JWEToken(Token):
    def __init__(self,
                 site='live',
                 token=None,
                 details=None):
        self.site = site
        self.token = token
        self.details = details
        super().__init__()

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
                username: str = os.environ.get('stage_user'),
                password: str = os.environ.get('stage_password'),
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
        self.details = {'request_headers': prepped.headers,
                        'request_body': prepped.body,
                        'request_url': prepped.url,
                        'response': response.status_code}


# to do: inherited JWE/bearer class
# add refresh function to both
# add local-load to both


if __name__ == '__main__':
    jwe_test = JWEToken()
    print(jwe_test.valid)
    print(jwe_test.expires_in)
    print(jwe_test.scope)
    print(jwe_test.site)
    print(jwe_test.check())
#    print(jwe_test.import_local())
    pprint(jwe_test.import_local())


#    test = Token('HOFER_pleitner', datetime.now(), 20, True)

#    for i in range(20):
#        test.check()
#        sleep(3.0)
#        print(i)
#        print('token scope: {scope}, created at:{created}, expires in {expires_in} seconds'.format(scope=test.scope,
#                                                                                                   created=test.created,
#                                                                                                   expires_in=test.expires_in))
#        if test.valid is True:
#            print('token is valid')
#        else:
#            print('token has expired!')
