
import requests
import simplejson as json
from exceptions import GettError

class GettResponse(object):
    def __init__(self, http_status, response):
        self.http_status = http_status
        self.string_response = response
        self.response = self._unserialize(response)

    def _unserialize(self, response):
        if response:
            try:
                return json.loads(response)
            except:
                return response
        return None

    def __str__(self):
        return self.string_response

    def __repr__(self):
        return "<GettResponse: %s>" % self.http_status


class BaseRequest(object):
    def __init__(self, *args, **kwargs):
        self.base_url = "https://open.ge.tt/1"

    def _make_request(self, endpoint, type='GET'):
        pass

    def get(self, endpoint, *args, **kwargs):
        endpoint = self.base_url + endpoint
        return self._make_request(endpoint, type='GET')

    def post(self, endpoint, d, *args, **kwargs):
        endpoint = self.base_url + endpoint
        if not isinstance(d, str):
            d = json.dumps(d)

        return self._make_request(endpoint, type='POST', data=d)

    def put(self, endpoint, d, *args, **kwargs):
        return self._make_request(endpoint, type='PUT', data=d)


class GettRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super(BaseRequest,self).__init__(*args, **kwargs)
        self.base_url = "https://open.ge.tt/1"
        self.endpoint = None
        self.type = None
        self.data = None

    def __str__(self):
        return "<GettRequest: %s %s>" % (self.type, self.endpoint)

    def __repr__(self):
        return "<GettRequest: %s %s>" % (self.type, self.endpoint)

    def _make_request(self, endpoint, **kwargs):
        status_code = None
        response = None

        self.endpoint = endpoint
        self.__dict__.update(kwargs)

        if self.type == "GET":
            response = requests.get(self.endpoint)
        elif self.type == "POST":
            response = requests.post(self.endpoint, data=self.data)
        elif self.type == "PUT":
            response = requests.put(self.endpoint, data=self.data)
        else:
            raise NotImplementedError("%s is not supported" % self.type)

        if response.status_code == requests.codes.ok:
            return GettResponse(response.status_code, response.content)
        else:
            raise GettError(response.status_code, self.endpoint, response.content)
