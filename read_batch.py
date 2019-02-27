import requests
import os
from pprint import pprint


fh = open('token.txt', mode='r')
token = fh.read()
token = token.rstrip()
scope = os.environ.get('stage_scope')

#print(token)

url = 'https://stage.connectedcooking.com/haccps'.rstrip()
headers = {'Authorization': 'Bearer ' + token,
           'scope': scope}
parameters = {'finished': 'true',
              'page': 0,
              'size': 10}


with requests.Session() as sess:
    sess.headers.update(headers)
    r = requests.Request(method='GET', url=url, data=parameters)
    prepped = sess.prepare_request(r)
    print('--------------------------')
    print('url requested:')
    print(prepped.url)
    print('--------------------------')
    print('request headers')
    pprint(prepped.headers)
    print('--------------------------')
    print('request body')
    pprint(prepped.body)
    response = sess.send(prepped)
    print('--------------------------')
    print('response code')
    print(response.status_code)
    print('--------------------------')
    print('full response')
    pprint(response.json())
