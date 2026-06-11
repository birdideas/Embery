import urllib, logging
from requests import Response, Session

_logger = logging.getLogger(__name__)

class APIResponse:
    def __init__(self, resp : Response):
        self._resp = resp

        stat = resp.json()["success"]
        _logger.debug(f"Success: {stat}")

    @property
    def status_code(self):
        return self._resp.status_code

    @property
    def content(self):
        return self._resp.content

    def json(self):
        return self._resp.json()

class ClientBase:
    API_BASE_URL = "https://www.new-embers.com/api/"

    def __init__(self):
        self._sess = Session()

    @property
    def cookies(self):
        return self._sess.cookies

    def get(self, url, strip = False, *args, **kwargs):
        endpoint = urllib.parse.urljoin(self.API_BASE_URL, url)
        _logger.debug(f"GET {endpoint}")

        if strip:
            return self._sess.get(endpoint, *args, **kwargs)
        else:
            return APIResponse(self._sess.get(endpoint, *args, **kwargs))

    def post(self, url, strip = False, *args, **kwargs):
        endpoint = urllib.parse.urljoin(self.API_BASE_URL, url)
        _logger.debug(f"POST {endpoint}")

        if strip:
            return self._sess.post(endpoint, *args, **kwargs)
        else:
            return APIResponse(self._sess.post(endpoint, *args, **kwargs))

