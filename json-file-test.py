import json
import datetime as dt
from pprint import pprint

with open('token.json') as fh:
    data = json.load(fh)
    print(type(data))
    pprint(data)
print(dt.datetime.strptime(data.get('valid_to'), '%Y-%m-%d %H:%M:%S.%f'))
