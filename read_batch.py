import requests
import json
import datetime as dt
import pandas as pd
from pprint import pprint
from authentication import get_bearer


def get_batches(*,
                stage: bool = True) -> dict:
    url = 'https://stage.connectedcooking.com/api/haccps' if stage else 'https://www.connectedcooking.com/api/haccps'
    with open('token.json') as fh:
        auth_file = json.load(fh)
    expiration = dt.datetime.strptime(auth_file.get('valid_to'), '%Y-%m-%d %H:%M:%S.%f')
    if expiration < dt.datetime.now():
        choice = input('Bearer token has expired {} - refresh? Y/N: '.format(expiration))
        if choice == 'N':
            quit()
        else:
            get_bearer()
    # needs elif --> token for correct env?
    else:
        pass
    with open('token.json') as fh:
        auth_file = json.load(fh)
    token = auth_file['token']
    scope = auth_file['details']['request_headers']['scope']
    headers = {'Authorization': 'Bearer ' + token,
               'scope': scope}
    parameters = {'finished': 'true',
                  'page': 0}
    with requests.Session() as sess:
        sess.headers.update(headers)
        r = requests.Request(method='GET',
                             url=url,
                             data=parameters)
        prepped = sess.prepare_request(r)
        response = sess.send(prepped)
    return {'response': response.status_code,
            'details': {'url': url,
                        'request_headers': dict(prepped.headers),
                        'request_body': prepped.body},
            'batches': response.json()}


if __name__ == '__main__':
    batches = get_batches(stage=True)
    pprint(batches.get('request_headers'))
    pprint(batches.get('request_body'))
    print(batches.get('response'))
    test = pd.DataFrame(batches.get('batches'))
    print(test.shape)
    print(test.head())
    test.to_csv('test_csv.csv')
