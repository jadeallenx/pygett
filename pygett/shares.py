from request import GettRequest
from files import GettFile


class GettShare(object):
    """
    Encapsulate a share in the Gett service.

    **Attributes**
        - ``sharename`` The sharename
        - ``title`` The share title (if any)
        - ``created`` Unix epoch seconds when the share was created
        - ``files`` A list of all files contained in a share as :py:mod:`pygett.files.GettFile` objects
    """
    def __init__(self, user, **kwargs):
        self.user = user
        self.sharename = None
        self.title = None
        self.created = None
        self.files = list()

        if 'files' in kwargs:
            files = kwargs['files']
            del kwargs['files']
            for f in files:
                if not 'sharename' in f:
                    f['sharename'] = kwargs['sharename']
                self.files.append(GettFile(self.user, **f))

        self.__dict__.update(kwargs)

    def __repr__(self):
        return "<GettShare: %s>" % self.sharename

    def __str__(self):
        return "<GettShare: %s>" % self.sharename

    def update(self, **kwargs):
        """
        Add, remove or modify a share's title.

        Input:
            * ``title`` The share title, if any (optional)

        **NOTE**: Passing ``None`` or calling this method with an empty argument list will remove the share's title.

        Output:
            * None

        Example::

            share = client.get_share("4ddfds")
            share.update(title="Example") # Set title to Example
            share.update()                # Remove title
        """
        if 'title' in kwargs:
            params = {"title": kwargs['title']}
        else:
            params = {"title": None}

        response = GettRequest().post("/shares/%s/update?accesstoken=%s" % (self.sharename, self.user.access_token()), params)

        if response.http_status == 200:
            self.__init__(self.user, **response.response)

    def destroy(self):
        """
        This method removes this share and all of its associated files. There is no way to recover a share or its contents
        once this method has been called.

        Input:
            * None

        Output:
            * ``True``

        Example::

            client.get_share("4ddfds").destroy()
        """
        response = GettRequest().post("/shares/%s/destroy?accesstoken=%s" % (self.sharename, self.user.access_token()), None)

        if response.http_status == 200:
            return True

    def refresh(self):
        """
        This method refreshes the object with current metadata from the Gett service.

        Input:
            * None

        Output:
            * None

        Example::

            share = client.get_share("4ddfds")
            print share.files[0].filename      # prints 'foobar'
            if share.files[0].destroy():
                share.refresh()
                print share.files[0].filename  # now prints 'barbaz'
        """
        response = GettRequest().get("/shares/%s" % self.sharename)

        if response.http_status == 200:
            self.__init__(self.user, **response.response)

