"""
Ge.tt Python bindings
:author Mark Allen
:version 0.1
"""

import re
import time

from user import GettUser
from request import GettRequest
from shares import GettShare
from files import GettFile

class Gett(object):
    def __init__(self, *args, **kwargs):
        self.required_params = [
            'apikey',
            'email',
            'password'
        ]

        self._check_params(**kwargs)
        self.user = GettUser(kwargs['apikey'], kwargs['email'], kwargs['password'])

    def _check_params(self,**kwargs):
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

    def get_shares(self, **kwargs):
        endpoint = "/shares?accesstoken=%s" % self.user.access_token
        if kwargs['limit'] and isinstance(kwargs['limit'], int) and kwargs['limit'] > 0:
            endpoint = endpoint + "&limit=%d" % kwargs['limit']
        if kwargs['skip'] and isinstance(kwargs['skip'], int) and kwargs['skip'] > 0:
            endpoint = endpoint + "&skip=%d" % kwargs['skip']

        response = GettRequest.get(endpoint)

        rv = list()

        if response.http_status == 200:
            for share in response.response:
                rv.append(GettShare(self.user, share))

            return rv

    def get_share(self, sharename):
        response = GettRequest.get("/shares/%s" % sharename)

        if response.http_status == 200:
            return GettShare(self.user, response.response)

    def get_file(self, sharename, fileid):
        response = GettRequest.get("/files/%s/%d" % (sharename, fileid))

        if response.http_status == 200:
            return GettFile(self.user, response.response)

