
import requests
import simplejson

class GettResponse(object):
    def __init__(self, http_status, response):
        self.http_status = http_status
        self.string_response = response
        self.response = self._unserialize(response)

    def _unserialize(self, response):
        if response:
            try:
                return json.dumps(response)
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
        self.endpoint = None
        self.type = None
        self.data = None

        self.__dict__.update(kwargs)

    def __make_request(self, endpoint, **kwargs):
        status_code = None
        response = None

        if self.type == "GET":
            response = requests.get(self.endpoint)
        else if self.type == "POST":
            response = requests.post(self.endpoint, data=self.data)
        else if self.type == "PUT":
            response = requests.put(self.endpoint, data=self.data)
        else:
            raise NotImplementedError("%s is not supported" % self.type)

        return GettResponse(response.status_code, response.content)
