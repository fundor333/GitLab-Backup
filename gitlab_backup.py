# -*- coding: utf-8 -*-
import json
import subprocess
import json
import io
import urllib, json
import urllib.parse
import urllib.request


try:
    with open("settings.json", "r") as stream:
        settings = json.load(stream)
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

for repo in settings["Repositories"]["Archived"]:
    bash_command = "git -C {} pull --all".format(
        settings["Repositories"]["Path"] + repo["path"]
    )
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


print("Starting the download")

url = settings["GitLab"]["Base url"] + "/api/v4/projects"
headers = {"Private-Token": settings["GitLab"]["Personal token"]}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    r = json.loads(response.read().decode())

    for repo in r:
        bash_command = "git clone --recurse-submodules {} {}".format(
            repo["http_url_to_repo"],
            settings["Repositories"]["Path"] + repo["path_with_namespace"],
        )
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        settings["Repositories"]["Archived"].append(
            {"url": repo["http_url_to_repo"], "path": repo["path_with_namespace"]}
        )

    with io.open("settings.json", "w") as outfile:
        json.dump(settings, outfile)
    exit()
