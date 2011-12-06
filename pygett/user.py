"""
Gett User class
"""

class User(Gett):
    def __init__(self, *args, **kwargs):
        self.userid = None
        self.fullname = None
        self.email = None
        self.storage_used = None
        self.storage_limit = None

        if kwargs:
            self.__dict__.update(**kwargs)

    def refresh(self):
        endpoint = "/users/me?accesstoken=%s" % self.access_token
        self.__dict__.update(self._send('GET', endpoint))

