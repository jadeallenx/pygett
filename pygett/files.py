from request import GettRequest

class GettFile(object):
    """
    Encapsulate a file in the Gett service.

    **Attributes**

    This object has the following attributes:
        - ``fileid`` - A file id as assigned by the Gett service
        - ``sharename`` - The sharename in which this file is contained
        - ``downloads`` - The number of downloads of this file
        - ``getturl`` - The URL at which this file can be viewed in a browser
        - ``filename`` - The user specified filename 
        - ``readystate`` - The Gett state of this file

    During file uploads, the following attributes will be set:
        - ``put_upload_url`` - A URL suitable for use with the PUT HTTP verb (see ``send_file()``)
        - ``post_upload_url`` - A URL suitable for use with the POST HTTP verb 
    """

    def __init__(self, user, **kwargs):
        self.user = user
        self.fileid = None
        self.sharename = None
        self.downloads = None
        self.getturl = None
        self.created = None
        self.filename = None
        self.readystate = None

        self.__dict__.update(kwargs)

        if 'upload' in kwargs:
            self.put_upload_url = kwargs['upload']['puturl']
            self.post_upload_url = kwargs['upload']['posturl']
        else:
            self.put_upload_url = None
            self.post_upload_url = None

    def __repr__(self):
        return "<GettFile: %s (%s/%s)>" % (self.filename, self.sharename, self.fileid)

    def __str__(self):
        return "<GettFile: %s (%s/%s)>" % (self.filename, self.sharename, self.fileid)

    def contents(self):
        """
        This method downloads the contents of the file represented by a `GettFile` object's metadata.

        Input:
            * None

        Output:
            * A byte stream

        **NOTE**: You are responsible for handling any encoding/decoding which may be necessary.

        Example::

            file = client.get_file("4ddfds", 0)
            print file.contents()
        """
        response = GettRequest().get("/files/%s/%s/blob" % (self.sharename, self.fileid))

        return response.response

    def thumbnail(self):
        """
        This method returns a thumbnail representation of the file if the data is a supported graphics format.

        Input:
            * None

        Output:
            * A byte stream representing a thumbnail of a support graphics file

        Example::

            file = client.get_file("4ddfds", 0)
            open("thumbnail.jpg", "wb").write(file.thumbnail())
        """
        response = GettRequest().get("/files/%s/%s/blob/thumb" % (self.sharename, self.fileid))

        return response.response

    def destroy(self):
        """
        This method removes the file's content and metadata from the Gett service.  There is no way to recover
        the data once this method has successfully completed.

        Input:
            * None

        Output:
            * ``True``

        Example::

            client.get_file("4ddfds", 0).destroy()
        """
        response = GettRequest().post(("/files/%s/%s/destroy?accesstoken=%s" % self.user.access_token()), None)

        if response.http_status == 200:
            return True

    def upload_url(self):
        """
        This method generates URLs which allow overwriting a file's content with new content. The output is suitable
        for use in the ``send_data()`` method below.

        Input:
            * None

        Output:
            * A URL (string)

        Example::

            file = client.get_file("4ddfds", 0)
            file.send_data(put_url=file.upload_url, data=open("example.txt", "rb").read())

        """
        if self.put_upload_url:
            return self.put_upload_url
        else:
            response = GettRequest().get("/files/%s/%s/upload?accesstoken=%s" % (self.sharename, self.fileid, self.user.access_token()))
            if response.http_status == 200:
                return response.response['puturl']

    def refresh(self):
        """
        Retrieve current file metadata from the Gett service.

        Input:
            * None

        Output:
            * None

        Example::

            file = client.get_file("4ddfds", 0)
            print "File size: %s" % file.size  # File size: 96
            file.send_data(put_url=file.upload_url, data=open("example.txt", "rb").read())
            file.refresh()
            print "File size: %s" % file.size  # File size: 109
        """
        response = GettRequest().get("/files/%s/%s" % (self.sharename, self.fileid))

        if response.http_status == 200:
            self.__init__(self.user, response.response)

    def send_data(self, **kwargs):
        """
        This method transmits data to the Gett service.

        Input:
            * ``put_url`` A PUT url to use when transmitting the data (required)
            * ``data`` A byte stream (required)

        Output:
            * ``True``

        Example::

            if file.send_data(put_url=file.upload_url, data=open("example.txt", "rb").read()):
                print "Your file has been uploaded."
        """
        put_url = None
        if 'put_url' in kwargs:
            put_url = kwargs['put_url']
        else:
            put_url = self.put_upload_url

        if 'data' not in kwargs:
            raise AttributeError("'data' parameter is required")

        if not put_url:
            raise AttributeError("'put_url' cannot be None")

        if not isinstance(kwargs['data'], str):
            raise TypeError("'data' parameter must be of type 'str'")

        response = GettRequest().put(put_url, kwargs['data'])

        if response.http_status == 200:
            return True
