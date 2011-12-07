"""
Gett User class
"""

import time
from request import GettRequest

class GettUser(object):
    def __init__(self, apikey, email, password):
        self.apikey = apikey
        self.email = email
        self.password = password
        self._access_token = None
        self.refresh_token = None
        self.access_token_expires = None
        self.access_token_grace = 3600
        self.userid = None
        self.fullname = None
        self.storage_used = None
        self.storage_limit = None

    def login(self, params):
        if not params:
            params = {
                apikey: self.apikey
                email: self.email
                password: self.password
            }

        response = GettRequest.post("/users/login", params)

        if response.http_status == 200:
            self._access_token = response.response['accesstoken']
            self.refresh_token = response.response['refreshtoken']
            self.access_token_expires = localtime() + response.response['expires']
            self.userid = response.response['user']['userid']
            self.fullname = response.response['user']['fullname']
            self.storage_used = response.response['user']['storage']['used']
            self.storage_limit = response.response['user']['storage']['limit']

    def access_token(self):
        if not self._access_token:
            self.login

        if localtime() > ( self.access_token_expires - self.access_token_grace ):
            self.login({ refreshtoken: self.refresh_token })

        return self._access_token

    def refresh_user(self):
        response = GettRequest.get("/users/me?accesstoken=%s" % self.access_token)

        if response.http_status == 200:
           self.userid = response.response['userid']
           self.fullname = response.response['fullname']
           self.storage_used = response.response['storage']['used']
           self.storage_limit = response.response['storage']['limit']
