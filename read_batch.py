import requests
import json
from pprint import pprint


with open('token.json', mode='r') as fh:
    auth_file = json.load(fh)

token = auth_file['token']
scope = auth_file['details']['request_headers']['scope']

url = 'https://stage.connectedcooking.com/api/haccps'
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
