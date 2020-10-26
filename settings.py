import io
import json


def get_settings():
    try:
        with open("settings.json", "r") as stream:
            settings = json.load(stream)
        return settings
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
        exit()
