# -*- coding: utf-8 -*-
import json
import subprocess
import json
import io
import urllib, json
import urllib.parse
import urllib.request
from datetime import datetime


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
            },
            "Repositories": {"Path": "repos/", "Archived": []},
        }
        with io.open("settings.json", "w", encoding="utf8") as outfile:
            json.dump(settings, outfile)
        exit()


def manage_repo(list_archived, settings, repo):
    if (
        settings["Repositories"]["Path"] + repo["path_with_namespace"]
        in list_archived.keys()
    ):
        print("{} is old repo".format(repo["path_with_namespace"]))
        bash_command = "git -C {} pull --all".format(
            settings["Repositories"]["Path"] + repo["path_with_namespace"]
        )

    else:
        print("{} is new repo".format(repo["path_with_namespace"]))
        bash_command = "git clone --recurse-submodules {} {}".format(
            repo["http_url_to_repo"],
            settings["Repositories"]["Path"] + repo["path_with_namespace"],
        )

        settings["Repositories"]["Archived"].append(
            {
                "url": repo["http_url_to_repo"],
                "path": settings["Repositories"]["Path"] + repo["path_with_namespace"],
            }
        )

    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    with io.open("settings.json", "w") as outfile:
        json.dump(settings, outfile)


if __name__ == "__main__":
    settings = get_settings()

    print("Starting the download")

    url = settings["GitLab"]["Base url"] + "/api/v4/projects?per_page=100"
    headers = {"Private-Token": settings["GitLab"]["Personal token"]}

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        r = json.loads(response.read().decode())
        list_archived = {}
        for e in settings["Repositories"]["Archived"]:
            list_archived[e["path"]] = e["url"]
        for repo in r:
            manage_repo(list_archived, settings, repo)

        settings["Last"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        with io.open("settings.json", "w") as outfile:
            json.dump(settings, outfile)
        exit()
