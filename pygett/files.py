"""
Ge.tt Python bindings
:author Mark Allen
:version 1.0
"""

from request import GettRequest

class GettFile(object):
    """
    ========
    GettFile
    ========

    Encapsulate a file in the Gett service.

    Attributes
    ==========

    This object has the following attributes:
    - ``fileid`` - A file id as assigned by the Gett service
    - ``sharename`` - The sharename in which this file is contained
    - ``downloads`` - The number of downloads of this file
    - ``getturl`` - The URL at which this file can be viewed in a browser
    - ``filename`` - The user specified filename 
    - ``readystate`` - The Gett state of this file

    During file uploads, the following attributes will be set:
    - ``put_upload_url`` - A URL suitable for use with the PUT HTTP verb (see ``send_file()``_)
    - ``post_upload_url`` - A URL suitable for use with the POST HTTP verb 

    Methods
    =======
    - ``contents()`` - Download the contents of this file
    - ``thumbnail()`` - Get a thumbnail of this file (if it is image data)
    - ``destroy()`` - Remove this file and its content from the Gett service
    - ``upload_url()`` - Get an upload_url to overwrite file's content
    - ``send_data()`` - Transmit data to the Gett service for this file's metadata
    - ``refresh()`` - Update file metadata from Gett service
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
        response = GettRequest().get("/files/%s/%s/blob" % (self.sharename, self.fileid))

        return response.response

    def thumbnail(self):
        response = GettRequest().get("/files/%s/%s/blob/thumb" % (self.sharename, self.fileid))

        return response.response

    def destroy(self):
        response = GettRequest().post(("/files/%s/%s/destroy?accesstoken=%s" % self.user.access_token()), None)

        if response.http_status == 200:
            return True

    def upload_url(self):
        if self.put_upload_url:
            return self.put_upload_url
        else:
            response = GettRequest().get("/files/%s/%s/upload?accesstoken=%s" % (self.sharename, self.fileid, self.user.access_token()))
            if response.http_status == 200:
                return response.response['puturl']

    def refresh(self):
        response = GettRequest().get("/files/%s/%s" % (self.sharename, self.fileid))

        if response.http_status == 200:
            self.__init__(self.user, response.response)

    def send_data(self, **kwargs):
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
