from class_token import JWEToken, BearerToken
from pprint import pprint


jwe_test = JWEToken()
#print(jwe_test.request())
#print(jwe_test.export_local('jwe.json'))
print(jwe_test.import_local('jwe.json'))
pprint(jwe_test.details)

bearer = BearerToken()
#print(bearer.request(jwe=jwe_test.token))
#print(bearer.export_local('bearer.json'))
print(bearer.import_local('bearer.json'))
pprint(bearer.details)

#pprint(bearer.details)
#print(type(bearer.valid_to))
#print(bearer.created)
#print(bearer.expires_in)
#print(bearer.check())
