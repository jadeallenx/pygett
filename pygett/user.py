from time import time
from pygett.request import GettRequest


class GettUser(object):
    """
    Encapsulates Gett user functionality

    **Attributes**
        - ``apikey`` The API key assigned by Gett for an application
        - ``email`` The email linked to the API key
        - ``password`` The password linked to the API key

    After a successful login the following attributes are populated:
        - ``refresh_token`` Used to get a new valid access token without requiring the API key, email and password
        - ``access_token_expires`` - Epoch seconds until the current access token is no longer valid. Typically 86400 seconds from login. (Suitable for use with ``time.localtime()``)
        - ``access_token_grace`` - How many seconds before an access token is scheduled to expire to attempt a renewal. (Defaults to 3600 seconds)
        - ``userid`` - User ID string supplied by Gett
        - ``fullname`` - The full name linked to an authenticated user account
        - ``storage_used`` - The amount of storage consumed (in total) for this user account. (Unit: bytes)
        - ``storage_limit`` - The maximum number of bytes available for storage. (Unit: bytes)
    """

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

    def __str__(self):
        if self.fullname:
            return "<GettUser: %s>" % self.fullname
        else:
            return "<GettUser: %s (not logged in)>" % self.email

    def __repr__(self):
        if self.fullname:
            return "<GettUser: %s>" % self.fullname
        else:
            return "<GettUser: %s (not logged in)>" % self.email

    def login(self, **params):
        """
        **login**

        Use the current credentials to get a valid Gett access token.

        Input:
            * A dict of parameters to use for the login attempt (optional)

        Output:
            * ``True``

        Example::

            if client.user.login():
                print "You have %s bytes of storage remaining." % ( client.user.storage_limit - client_user.storage_used )
        """

        if not params:
            params = {
                "apikey": self.apikey,
                "email": self.email,
                "password": self.password
            }

        response = GettRequest().post("/users/login", params)

        if response.http_status == 200:
            self._access_token = response.response['accesstoken']
            self.refresh_token = response.response['refreshtoken']
            self.access_token_expires = int(time()) + response.response['expires']
            self.userid = response.response['user']['userid']
            self.fullname = response.response['user']['fullname']
            self.storage_used = response.response['user']['storage']['used']
            self.storage_limit = response.response['user']['storage']['limit']

            return True

    def access_token(self):
        """
        **access_token**

        Returns a valid access token.  If the user is not currently logged in, attempts to do so.
        If the current time exceeds the grace period, attempts to retrieve a new access token.

        Input:
            * None

        Output:
            * A valid access token

        Example::

            print "Your access token is currently %s" % client.user.access_token()
        """
        if not self._access_token:
            self.login()

        if time() > (self.access_token_expires - self.access_token_grace):
            self.login({"refreshtoken": self.refresh_token})

        return self._access_token

    def refresh(self):
        """
        **refresh**

        Refresh this user object with data from the Gett service

        Input:
            * None

        Output:
            * ``True``

        Example::

            if client.user.refresh():
                print "User data refreshed!"
                print "You have %s bytes of storage remaining." % ( client.user.storage_limit - client_user.storage_used )

        """
        response = GettRequest().get("/users/me?accesstoken=%s" % self.access_token())

        if response.http_status == 200:
            self.userid = response.response['userid']
            self.fullname = response.response['fullname']
            self.storage_used = response.response['storage']['used']
            self.storage_limit = response.response['storage']['limit']

            return True
