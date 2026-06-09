import logging, os

import requests, dotenv

s = requests.Session()
logger = logging.getLogger(__name__)

def get_my_balances():
    logging.debug("Hitting getMyBalances...")
    ret = s.get("https://www.new-embers.com/api/users/getMyBalances")

    logging.debug(f"Request done. Got code {ret.status_code}")
    if ret.status_code >= 200 and ret.status_code <= 299:
        logging.critical("Uh oh")

    return ret

def login(url : str):
    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    password_redacted = '********'

    logging.debug("Hitting CSRF endpoint...")
    csrf_response = s.get("https://www.new-embers.com/api/auth/csrf")
    csrf_token = csrf_response.json()["csrfToken"]
    if not csrf_token:
        raise RuntimeError
    logging.debug(f"Got CSRF token: {csrf_token}")

    logging.debug(f"Posting to endpoint: {url}")
    logging.debug(f"User: {username}  Password: {password_redacted}")

    logging.debug("Posting now...")
    ret = s.post(
        url,

        data = {
            "email": username,
            "password": password,
            "redirect": "false",
            "csrfToken": csrf_token,
            # "callbackUrl": "https://www.new-embers.com/auth/signin",
            "json": "true",
        },
    )

    logging.debug(f"Request done. Got code {ret.status_code}")
    if ret.status_code >= 200 and ret.status_code <= 299:
        logging.critical("Uh oh")

    logging.debug(s.cookies)

    return ret

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger.info("Loading environment variables")
    dotenv.load_dotenv()

    if not (os.getenv("EMAIL") and os.getenv("PASSWORD")):
        logger.critical("Could not load credentials from dotenv!")
        raise RuntimeError

    base_url = "https://www.new-embers.com/"
    sess_url = "api/auth/callback/credentials"

    ret = login(base_url + sess_url)
    logging.debug(ret.content)

    ret = get_my_balances()
    logging.debug(ret.content)

