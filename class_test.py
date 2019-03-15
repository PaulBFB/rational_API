from token_class import JWEToken, BearerToken
from pprint import pprint


jwe_test = JWEToken()
print(jwe_test.request())
print(jwe_test.export_local())
print(jwe_test.import_local())
pprint(jwe_test.details)

bearer = BearerToken()
print(bearer.request(jwe=jwe_test.token))
print(bearer.export_local())
print(bearer.import_local())
pprint(bearer.details)

#pprint(bearer.details)
#print(type(bearer.valid_to))
#print(bearer.created)
#print(bearer.expires_in)
#print(bearer.check())
