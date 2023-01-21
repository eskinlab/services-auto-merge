# -*- coding: utf-8 -*-
from os import getenv

GITLAB = {
    'url': "http://gitlab_url",
    'token': getenv('GITLAB_TOKEN')
}

SOURCE_FILE = {
    'project': "kk/devops",
    'name': 'actual_version.ini',
    'branch': 'master'
}

GRADLE_FILE = "gradle.properties"
SNAPSHOT_PATTERN = "-SNAPSHOT"

# Logger settings
LOGS = {
    "level": "INFO",
    "format": f"\n%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
}
