import json
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from pprint import pprint


time_format = '%Y-%m-%d %H:%M:%S.%f'            # used for json Imports


class Token:
    """Parent class of all token Types used in the rational ConnectedCooking API

    Attributes:
        :param scope (str): token scope - sent to REST API in headers (default: retrieved from os.environ[stage_scope])
        :param created (datetime.datetime): automatically set - when the token was initialized (default: now())
        :param valid (bool): if token is valid (default: None)
        :param site (str): indicating if production/staging is called (default: 'live')
        :param token (str): token as string (default: None)
    """

    def __init__(self,
                 scope=os.environ.get('stage_scope'),
                 created=datetime.now(),
                 valid=None,
                 details=None,
                 site='live',
                 token=None):
        self.scope = scope
        self.created = created
        self.valid = valid
        self.details = details
        self.site = site
        self.token = token

    def export_local(self, path=None):
        """exports the current parameters of the token Object to a local JSON file

        Parameters:
            :param path: the file path to be saved (default: 'token.json')
            :type path: str
        :returns True/False
        """

        if path is None:
            path = 'token.json'         # default variable does not work in class method, workaround
        data = {'token': self.token,
                'created': str(self.created),
                'details': self.details}
        with open(path, mode='w') as fh:
            json.dump(data, fh)
        return True

    def import_local(self, path=None):
        """imports token from a local JSON file and sets all object parameters if unsuccessful, sets token.valid=False

        Parameters:
            :param path: the file path to be imported from (default: 'token.json')
        :returns: True/False
        """

        if path is None:
            path = 'token.json'
        try:
            with open(path) as fh:
                local = json.load(fh)
            self.token = local['token']
            self.details = local['details']
            self.created = datetime.strptime(local['created'], time_format)
            self.valid = True
            return True
        except FileNotFoundError:
            self.valid = False
            return False


class JWEToken(Token):
    """subclass - used for authorisation
    """

    def request(self, *,
                username: str = os.environ.get('live_user'),
                password: str = os.environ.get('live_password'),
                scope=None,
                url: str = 'https://www.club-rational.com/member/loginCC'):
        """retrieves a JWE token from the API based on user/password

        Parameters:
            :param username: user in auth (default: retrieved from os.environ['live_user'])
            :param password: password in auth (default: retrieved from os.environ['live_password'])
            :param scope: scope parameter to be sent with request (default: self.scope/'HOFER_pleitner')
            :param url: request url (default: 'https://www.club-rational.com/member/loginCC')
         :returns True/False   """

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


class BearerToken(Token):
    """subclass used for Bearer Token - additional parameters

    Parameters:
        :param refresh_token (str): refresh token from latest request (default: None)
        :param valid_to (datetime.datetime): expiration datetime - set at request with sec offset (default: None)


    """
    def __init__(self,
                 refresh_token=None,
                 valid_to=None):
        super().__init__()          # inherits all parameters from parent class + additional parameters
        self.refresh_token = refresh_token
        self.valid_to = valid_to

    def import_local(self,
                     path=None):
        """imports token from a local JSON file and sets all object parameters if unsuccessful, sets token.valid=False

        Parameters:
            :param path: the file path to be imported from (default: 'token.json')
        :returns: True/False
        """

        if path is None:
            path = self.site + '_bearer_token.json'
        if super().import_local(path=path):         # inherits all parameters from super().import_local()
            with open(path) as fh:
                local = json.load(fh)
            self.refresh_token = local['refresh_token']
            self.valid_to = datetime.strptime(local['valid_to'], time_format)
            return True
        else:           # if super().import_local with path fails, set valid to False
            self.valid = False
            return False

    def export_local(self,
                     path=None):
        """exports the current parameters of the token Object to a local JSON file

        Parameters:
            :param path: the file path to be saved (default: 'token.json')
            :type path: str
        :returns True/False
        """

        if path is None:
            path = self.site + '_bearer_joken.json'
        data = {'token': self.token,
                'details': self.details,
                'created': str(self.created),
                'valid_to': str(self.valid_to),
                'refresh_token': self.refresh_token}
        try:
            with open(path, mode='w') as fh:
                json.dump(data, fh)
            return True
        except FileExistsError:
            return False

    def request(self,
                jwe: str,
                client_id: str = os.environ.get('live_client_id'),
                client_secret: str = os.environ.get('live_client_secret'),
                scope: str = os.environ.get('stage_scope'),
                url: str = 'https://www.connectedcooking.com/oauth/token'):
        """
        creates a bearer token based on jwe token, client secret/id

        Parameters:
            :param jwe: valid jwe token, get from JWEToken.token
            :param client_id: client id for API (default: retrieved from os.environ['live_client_id'])
            :param client_secret: client secret for API (default: retrieved from os.environ['live_client_secret'])
            :param scope: scope parameter to be sent with request (default: self.scope/'HOFER_pleitner')
            :param url: request url (default: 'https://www.connectedcooking.com/oauth/token')
        :returns: True/False
        """

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

    def check(self):
        """checks if valid_to date is in the past, sets self.valid True/False
        :returns: bool
        """

        if self.valid_to > datetime.now():
            self.valid = True
            return True

        else:
            self.valid = False
            return False


if __name__ == '__main__':
    jwe_test = JWEToken()
    print(jwe_test.valid)
    print(jwe_test.scope)
    print(jwe_test.site)
    pprint(jwe_test.import_local())
