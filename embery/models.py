from requests import Response, Session

class APIResponse:
    def __init__(self, resp : Response):
        self._resp = resp

    @property
    def status_code(self):
        return self._resp.status_code

    @property
    def content(self):
        return self._resp.content

    def json(self):
        return self._resp.json()

class ClientBase:
    def __init__(self):
        self._sess = Session()

    @property
    def cookies(self):
        return self._sess.cookies

    def get(self, *args, **kwargs):
        return APIResponse(self._sess.get(*args, **kwargs))

    def post(self, *args, **kwargs):
        return APIResponse(self._sess.post(*args, **kwargs))

