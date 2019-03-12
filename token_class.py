from datetime import datetime, timedelta
from time import sleep


class Token:
    def __init__(self, scope='live', created=datetime.now(), expires_in=100, valid=True):
        self.scope = scope
        self.created = created
        self.expires_in = expires_in
        self.valid = valid

    def check(self):
        if self.created + timedelta(seconds=self.expires_in) > datetime.now():
            self.valid = True
        else:
            self.valid = False


# to do: inherited JWE/bearer class
# add refresh function to both
# add local-load to both

if __name__ == '__main__':
    test = Token('live', datetime.now(), 20, True)

    for i in range(20):
        test.check()
        sleep(3.0)
        print(i)
        print('token scope: {scope}, created at:{created}, expires in {expires_in} seconds'.format(scope=test.scope,
                                                                                                   created=test.created,
                                                                                                   expires_in=test.expires_in))
        if test.valid is True:
            print('token is valid')
        else:
            print('token has expired!')
