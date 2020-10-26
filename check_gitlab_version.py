from base64 import urlsafe_b64encode

import requests
from loguru import logger

from settings import get_settings


def get_gitlab_version():
    settings = get_settings()

    logger.info("Starting the download")

    url = settings["GitLab"]["Base url"] + "/api/v4/version"
    headers = {"Private-Token": settings["GitLab"]["Personal token"]}
    req = requests.get(url, headers=headers)
    return req.json()


def last_version_gitlab(s):
    settings = get_settings()
    url = settings["GitLab"]["Base url"]
    var = s["version"]
    gfg = urlsafe_b64encode(str.encode('{"version":"' + str(var) + '"}'))
    logger.debug(gfg)
    r = requests.get(url="https://version.gitlab.com/check.svg", params={'gitlab_info': gfg}, headers={'Referer': url})
    return "up-to-date" in r.text


if __name__ == "__main__":
    gitlab_version = get_gitlab_version()
    logger.info(gitlab_version)
    lvg = last_version_gitlab(gitlab_version)
    logger.info(lvg)
    if lvg:
        print("All Update")
    else:
        print("To Update")
