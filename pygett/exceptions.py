import simplejson as json

class GettError(Exception):
    def __init__(self, status_code, endpoint, params):
        self.http_status = status_code
        self.endpoint = endpoint
        self.error = None

        if isinstance(params, str):
            try:
                self.__dict__.update(json.loads(params))
            except JSONDecodeError:
                self.error = http_status

    def __str__(self):
        return "<GettError: %s>" % self.error

    def __repr__(self):
        return "<GettError: %s>" % self.error

