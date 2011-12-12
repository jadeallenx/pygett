"""
Ge.tt Python bindings 
author: Mark Allen
version: 1.0
"""
import simplejson as json

class GettError(Exception):
    """
    =========
    GettError
    =========

    Attributes
    ==========

    - ``http_status`` The HTTP status code from the remote server
    - ``endpoint`` The URI to which a request was attempted
    - ``error`` A message describing the error
    """
    def __init__(self, status_code, endpoint, params):
        self.http_status = status_code
        self.endpoint = endpoint
        self.error = None

        if isinstance(params, str):
            try:
                self.__dict__.update(json.loads(params))
            except:
                self.error = params

    def __str__(self):
        return "<GettError: (%s) %s>" % (self.http_status, self.error)

    def __repr__(self):
        return "<GettError: (%s) %s>" % (self.http_status, self.error)

