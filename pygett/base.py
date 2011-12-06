"""
Ge.tt Python bindings
:author Mark Allen
:version 0.1
"""

import re
import requests
import simplejson

class Gett(object):
    def __init__(self, *args, **kwargs):
        self.test_mode = False
        self.apikey = None
        self.email = None
        self.password = None
        self.base_url = 'https://open.ge.tt/1'
        self.required_params = [
            'apikey',
            'email',
            'password'
        ]

        self.access_token = None
        self.refresh_token = None
        self.access_token_expires = None

        self.check_params(**kwargs)
        self.__dict__.update(**kwargs)

    def check_params(self,**kwargs):
        if not kwargs:
            raise AttributeError('Missing required parameters: %s' % self.required_params)

        for param in self.required_params:
            if param not in kwargs:
                raise AttributeError('Missing required parameter %s' % param)

        for k, v in kwargs.items():
            if not v:
                raise AttributeError('Parameter %s must not be None' % k)
            if k == 'apikey':
                if not isinstance(v, str):
                    raise AttributeError("Parameter 'apikey' must be a string")
            if k == 'email':
                if not re.search(r'\w+@\w+', v):
                    raise AttributeError("Parameter 'email' must be an email address")
            if k == 'password':
                if not isinstance(v, str):
                    raise AttributeError("Parameter 'password' must be a string")

    def _send(self, method, endpoint, jsonstr):
        response = None
        if method == "GET":
            response = requests.get(endpoint)
        else if method == "POST":
            response = requests.post(endpoint, data=jsonstr)
        else:
            raise NotImplementedError("method %s is not implemented in this method" % method)

        if response.status_code == requests.codes.ok:
            return simplejson.dumps(response.contents)
        else:
            response.raise_for_status()



