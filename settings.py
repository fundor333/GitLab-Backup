import io
import json
import sys

from loguru import logger


def get_settings():
    settings = None
    try:
        with open("settings.json", "r") as stream:
            settings = json.load(stream)
    except FileNotFoundError:
        settings = {
            "GitLab": {
                "Base url": "https://gitlab.com",
                "Personal token": "<PUT HERE THE TOKEN>",
                "logger_level" : "ERROR",
            },
            "Repositories": {"Path": "repos/", "Archived": []},
        }
        with io.open("settings.json", "w", encoding="utf8") as outfile:
            json.dump(settings, outfile)
    finally:
        logger.remove()
        logger.add(sys.stderr, level="ERROR")
        logger.add(sys.stdout, level=settings['GitLab']['logger_level'])
    return settings
