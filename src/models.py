from requests import Response

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

