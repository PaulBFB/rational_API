from datetime import datetime, timedelta
from time import sleep


class Token:
    def __init__(self, scope='HOFER_pleitner', created=datetime.now(), expires_in=86400, valid=True):
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
    def __init__(self, site='live', token=None):
        self.site = site
        self.token = token
        super().__init__()

    def import_local(self,
                     path=None):
        if path is None:
            path = self.site + '_jwe_token.json'
        return path

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
    print(jwe_test.import_local())


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
