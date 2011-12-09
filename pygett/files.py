from request import GettRequest

class GettFile(object):
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
        if kwargs['put_url']:
            put_url = kwargs['put_url']
        elif self.put_upload_url:
            put_url = self.put_upload_url
        else:
            raise AttributeError("'put_url' cannot be None")

        response = GettRequest().put(put_url, kwargs['data'])

        if response.http_status == 200:
            return True
