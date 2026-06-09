import logging, os

import requests, dotenv

from embery import models

logger = logging.getLogger(__name__)

class Client(models.ClientBase):
    def test_open_pack(self, url : str):
        logging.debug(f"Hitting {url}...")
        resp = models.APIResponse(self.post(url))

        logging.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logging.critical("Uh oh")

        return resp

    def get_my_balances(self):
        logging.debug("Hitting getMyBalances...")
        ret = self.get("https://www.new-embers.com/api/users/getMyBalances")

        logging.debug(f"Request done. Got code {ret.status_code}")
        if not (ret.status_code >= 200 and ret.status_code <= 299):
            logging.critical("Uh oh")

        return ret

    def login(self, url : str):
        username = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        password_redacted = '********'

        logging.debug("Hitting CSRF endpoint...")
        csrf_response = models.APIResponse(self.get("https://www.new-embers.com/api/auth/csrf"))
        csrf_token = csrf_response.json()["csrfToken"]
        if not csrf_token:
            raise RuntimeError
        logging.debug(f"Got CSRF token: {csrf_token}")

        logging.debug(f"Posting to endpoint: {url}")
        logging.debug(f"User: {username}  Password: {password_redacted}")

        logging.debug("Posting now...")
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

        logging.debug(f"Request done. Got code {ret.status_code}")
        if ret.status_code >= 200 and ret.status_code <= 299:
            logging.critical("Uh oh")

        logging.debug(self.cookies)

        return ret

