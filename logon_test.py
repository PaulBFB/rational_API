import requests
import os
from authentication import get_bearer
from pprint import pprint
import json


# logon_url_live = 'https://www.club-rational.com/member/loginCC'
# url = logon_url_live
# user = os.environ['live_user']
# password = os.environ['live_password']
# login_test = cc_login(url=url,
#                       username=user,
#                       password=password)
# with open('token_test.json', mode='w') as fh:
#     json.dump(login_test, fh)


with open('token_test.json') as fh:
    token = json.load(fh)

token_url_live = 'https://www.connectedcooking.com/oauth/token'
#pprint(token)

#bearer = get_bearer(jwe=token['jwe'],
#                    url=token_url_live,
#                    client_secret=os.environ['live_client_secret'],
#                    client_id=os.environ['live_client_id'],
#                    scope=os.environ['stage_scope'])
#
#pprint(bearer)

with requests.Session() as sess:
    data = {'client_secret': os.environ['live_client_secret'],
            'client_id': os.environ['live_client_id'],
            'grant_type': 'jwe_token',
            'jwe': token['jwe']}
    r = requests.Request(method='POST',
                         url=token_url_live,
                         data=data)
    prepped = sess.prepare_request(r)
    response = sess.send(prepped)
    pprint(response.json())
