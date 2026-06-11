import logging, os

import requests, dotenv

from embery import models

logger = logging.getLogger(__name__)

class Client(models.ClientBase):
    def test_open_pack(self, url : str):
        resp = self.post(url)

        logger.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logger.critical("Uh oh")

        return resp

    def get_series(self, series_id):
        endpoint = f"series/{series_id}/get"
        return self.get(endpoint)

    def get_my_balances(self):
        endpoint = "users/getMyBalances"
        ret = self.get(endpoint)

        logger.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logger.critical("Uh oh")

        return ret

    def login(self, url : str):
        endpoint = "auth/csrf"

        username = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        password_redacted = '********'

        csrf_response = self.get(endpoint, strip = True)
        csrf_token = csrf_response.json()["csrfToken"]
        if not csrf_token:
            raise RuntimeError
        logger.debug(f"Got CSRF token: {csrf_token}")

        logger.debug(f"Posting to endpoint: {url}")
        logger.debug(f"User: {username}  Password: {password_redacted}")

        logger.debug("Posting now...")
        ret = self.post(
            url,

            data = {
                "email": username,
                "password": password,
                "redirect": "false",
                "csrfToken": csrf_token,
                # "callbackUrl": "https://www.new-embers.com/auth/signin",
                "json": "true",
            },

            strip = True
        )

        logger.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logger.critical("Uh oh")

        logger.debug(self.cookies)

        return ret

