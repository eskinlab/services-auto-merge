from os import getenv

GIT = {
    "user": getenv('GITLAB_USER'), # "someuser",
    "email": getenv('GITLAB_EMAIL'), # "somemail@sm.sm",
    "commit_msg": "Pre-Merge Update"
}

GITLAB = {
    'protocol': "http",
    'url': "gitlab.ru-central1.internal",
    'token': getenv('GITLAB_TOKEN'),
    "automerge_title": "Automerge failure"
}

BITBUCKET = {
    'protocol': "https",
    'url': "https://bitbucket_url/",
    'user': "",
    "password": "",
    "automerge_title": "Automerge failure"
}

SERVISES_FILE = {
    "serviceGroup": "kk",
    "serviceName": "devops",
    'branch':  'master',  # 'tst',
    "fileName": "services.json"
}
SERVICES_TYPE = {
    "mr-set": ["services_mr"],
    "branch-set": ["models"],
    "general": ["commons", "services", "emulators", "models"],
}

UPDATE_FILE = {
    'up_version_or_rm_snapshot': 'gradle.properties',
    'up_semantic_version': 'semantic-build-versioning.gradle',
    'up_ui_version': 'version-settings.json'
}

CURRENT_STAGE = getenv('CI_JOB_STAGE') # "models"
CURRENT_DIR = getenv('CI_PROJECT_DIR') # "../../"
PYTHON = "python"

# Logger settings
LOGS = {
    "level": "INFO",
    "format": f"\n%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
}
