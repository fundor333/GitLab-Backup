# -*- coding: utf-8 -*-
import json
import subprocess

import requests
import yaml

import io


try:
    with open("settings.yaml", "r") as stream:
        settings = yaml.load(stream)
except FileNotFoundError:
    settings = {
        "GitLab": {
            "Base url": "https//gitlab.com",
            "Personal token": "<PUT HERE THE TOKEN>",
        },
        "Repositories": {"Path": "repos/", "Archived": []},
    }
    with io.open("settings.yaml", "w", encoding="utf8") as outfile:
        yaml.dump(settings, outfile, default_flow_style=False, allow_unicode=True)
    exit()

url = settings["GitLab"]["Base url"] + "/api/v4/projects"
headers = {"Private-Token": settings["GitLab"]["Personal token"]}

for repo in settings["Repositories"]["Archived"]:
    bash_command = "git -C {} pull --all".format(repo["path"])
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

r = requests.get(url, headers=headers).json()

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

"""
except Exception:
    print("The settings.yaml is wrong. Fix it")
"""

with io.open("settings.yaml", "w", encoding="utf8") as outfile:
    yaml.dump(settings, outfile, default_flow_style=False, allow_unicode=True)
exit()
