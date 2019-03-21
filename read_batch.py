import requests
import pandas as pd
from pprint import pprint
from token_class import JWEToken, BearerToken


jwe = JWEToken()
jwe.import_local('jwe_test.json')
bearer = BearerToken()
bearer.import_local('bearer_test.json')


def get_batches():
    url = 'https://www.connectedcooking.com/api/haccps'
    token = bearer.token
    scope = bearer.scope
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
    batches = get_batches()
    pprint(batches.get('request_headers'))
    pprint(batches.get('request_body'))
    print(batches.get('response'))
    test = pd.DataFrame(batches.get('batches'))
    print(test.shape)
    print(test.head())
    test.to_csv('test_csv.csv')
