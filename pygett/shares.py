from request import GettRequest
from files import GettFile

class GettShare(object):
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
        if 'title' in kwargs:
            params = { "title": kwargs['title'] }
        else:
            params = { "title": None }

        response = GettRequest().post("/shares/%s/update?accesstoken=%s" % (self.sharename, self.user.access_token()), params)

        if response.http_status == 200:
            self.__init__(self.user, **response.response)

    def destroy(self):
        response = GettRequest().post("/shares/%s/destroy?accesstoken=%s" % (self.sharename, self.user.access_token()), None)

        if response.http_status == 200:
            return True

    def refresh(self):
        response = GettRequest().get("/shares/%s" % self.sharename)

        if response.http_status == 200:
            self.__init__(self.user, **response.response)

