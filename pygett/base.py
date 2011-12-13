import re
import time

from user import GettUser
from request import GettRequest
from shares import GettShare
from files import GettFile


class Gett(object):
    """
    Base client object

    Requires the following keyword arguments:
        - ``apikey`` - The API key assigned to an application by Gett
        - ``email`` - The email address linked to the API key
        - ``password`` - The password linked to the API key

    **Attribute**
        - ``user`` - a :py:mod:`pygett.user.GettUser` object
    """

    def __init__(self, *args, **kwargs):
        self.required_params = [
            'apikey',
            'email',
            'password'
        ]

        self._check_params(**kwargs)
        self.user = GettUser(kwargs['apikey'], kwargs['email'], kwargs['password'])

    def _check_params(self, **kwargs):
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

    def _get_shares(self, **kwargs):
        endpoint = "/shares?accesstoken=%s" % self.user.access_token()
        if 'limit' in kwargs and isinstance(kwargs['limit'], int) and kwargs['limit'] > 0:
            endpoint = endpoint + "&limit=%d" % kwargs['limit']
        if 'skip' in kwargs and isinstance(kwargs['skip'], int) and kwargs['skip'] > 0:
            endpoint = endpoint + "&skip=%d" % kwargs['skip']

        return GettRequest().get(endpoint)

    def get_shares(self, **kwargs):
        """
        Gets *all* shares.

        Input:
            * ``skip`` the number of shares to skip (optional)
            * ``limit`` the maximum number of shares to return (optional)

        Output:
            * a dict where keys are sharenames and the values are corresponding :py:mod:`pygett.shares.GettShare` objects

        Example::

            shares = client.get_shares()
        """

        response = self._get_shares(**kwargs)

        rv = dict()

        if response.http_status == 200:
            for share in response.response:
                rv[share['sharename']] = GettShare(self.user, **share)

            return rv

    def get_shares_list(self, **kwargs):
        """
        Gets *all* shares.

        Input:
            * ``skip`` the number of shares to skip (optional)
            * ``limit`` the maximum number of shares to return (optional)

        Output:
            * a list of :py:mod:`pygett.shares.GettShare` objects

        Example::

            shares_list = client.get_shares_list()
        """

        response = self._get_shares(**kwargs)

        rv = list()

        if response.http_status == 200:
            for share in response.response:
                rv.append(GettShare(self.user, **share))

            return rv

    def get_share(self, sharename):
        """
        Get a specific share. Does not require authentication.

        Input:
            * A sharename

        Output:
            * A :py:mod:`pygett.shares.GettShare` object

        Example::

            share = client.get_share("4ddfds")
        """

        response = GettRequest().get("/shares/%s" % sharename)

        if response.http_status == 200:
            return GettShare(self.user, **response.response)

    def get_file(self, sharename, fileid):
        """
        Get a specific file. Does not require authentication.

        Input:
            * A sharename
            * A fileid - must be an integer

        Output:
            * A :py:mod:`pygett.files.GettFile` object

        Example::

            file = client.get_file("4ddfds", 0)
        """

        if not isinstance(fileid, int):
            raise TypeError("'fileid' must be an integer")

        response = GettRequest().get("/files/%s/%d" % (sharename, fileid))

        if response.http_status == 200:
            return GettFile(self.user, **response.response)

    def create_share(self, **kwargs):
        """
        Create a new share. Takes a keyword argument.

        Input:
            * ``title`` optional share title (optional)

        Output:
            * A :py:mod:`pygett.shares.GettShare` object

        Example::

            new_share = client.create_share( title="Example Title" )
        """

        params = None
        if 'title' in kwargs:
            params = {"title": kwargs['title']}

        response = GettRequest().post(("/shares/create?accesstoken=%s" % self.user.access_token()), params)

        if response.http_status == 200:
            return GettShare(self.user, **response.response)

    def upload_file(self, **kwargs):
        """
        Upload a file to the Gett service. Takes keyword arguments.

        Input:
            * ``filename`` the filename to use in the Gett service (required)
            * ``data`` the file contents to store in the Gett service (required) - must be a string
            * ``sharename`` the name of the share in which to store the data (optional); if not given, a new share will be created.
            * ``title`` the share title to use if a new share is created (optional)

        Output:
            * A :py:mod:`pygett.files.GettFile` object

        Example::

            file = client.upload_file(filaname="foo", data=open("foo.txt").read())
        """
        params = None
        if 'filename' not in kwargs:
            raise AttributeError("Parameter 'filename' must be given")
        else:
            params = {
                "filename": kwargs['filename']
            }

        if 'data' not in kwargs:
            raise AttributeError("Parameter 'data' must be given")

        sharename = None
        if 'sharename' not in kwargs:
            share = None
            if 'title' in kwargs:
                share = self.create_share(title=kwargs['title'])
            else:
                share = self.create_share()
            sharename = share.sharename
        else:
            sharename = kwargs['sharename']

        response = GettRequest().post("/files/%s/create?accesstoken=%s" % (sharename, self.user.access_token()), params)

        f = None
        if response.http_status == 200:
            if 'sharename' not in response.response:
                response.response['sharename'] = sharename
            f = GettFile(self.user, **response.response)
            if f.send_data(data=kwargs['data']):
                return f

