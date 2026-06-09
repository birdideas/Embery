import logging, os

import requests, dotenv

from embery import models

logger = logging.getLogger(__name__)

class Client(models.ClientBase):
    def test_open_pack(self, url : str):
        logger.debug(f"Hitting {url}...")
        resp = models.APIResponse(self.post(url))

        logger.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logger.critical("Uh oh")

        return resp

    def get_my_balances(self):
        logger.debug("Hitting getMyBalances...")
        ret = self.get("https://www.new-embers.com/api/users/getMyBalances")

        logger.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logger.critical("Uh oh")

        return ret

    def login(self, url : str):
        username = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        password_redacted = '********'

        logger.debug("Hitting CSRF endpoint...")
        csrf_response = models.APIResponse(self.get("https://www.new-embers.com/api/auth/csrf"))
        csrf_token = csrf_response.json()["csrfToken"]
        if not csrf_token:
            raise RuntimeError
        logger.debug(f"Got CSRF token: {csrf_token}")

        logger.debug(f"Posting to endpoint: {url}")
        logger.debug(f"User: {username}  Password: {password_redacted}")

        logger.debug("Posting now...")
        ret = models.APIResponse(self.post(
            url,

            data = {
                "email": username,
                "password": password,
                "redirect": "false",
                "csrfToken": csrf_token,
                # "callbackUrl": "https://www.new-embers.com/auth/signin",
                "json": "true",
            },
        ))

        logger.debug(f"Request done. Got code {ret.status_code}")
        if ret.status_code >= 200 and ret.status_code <= 299:
            logger.critical("Uh oh")

        logger.debug(self.cookies)

        return ret

