# Auto Merge Servises for Gitlab or Bitbucket

### Description

1. The script execute branches merge and releases in
   Gitlab and BitBucket version control systems
2. gradle.properties file edit:  
    -  up version till level specified in file actual_version.ini  
    -  remove word -SNAPSHOT
3. semantic-build-versioning.gradle file edit
   -  up version till release level


Functional launch is made from a CI/CD playbook with the following variables.
### The table of input CI/CD variables

| Name | Description | Default value |
| --- | --- | --- |
| `SYSTEM` | Version control system (gitlab, bitbucket) | gitlab |
| `BRANCH_FROM` | Branch From | - |
| `BRANCH_TO` | Branch To | - |
| `UP_VERSION` | if True - up versions in gradle.properties according to actual_version.ini | False |
| `RM_SNAPSHOT` | if True - cut out parameter -SNAPSHOT if the file gradle.properties | False |
| `UP_SEMANTIC_VERSION` | if True - set/up release version in semantic-build-versioning.gradle| False |
| `TELEGRAM_CHAT_ID` | ID Telegram chat, set in environment variables | - |


### Services list format in services.json
```sh
   {
      "serviceName": "",
      "serviceGroup": "",
	  "repoMaintainer": "",
	  "telegramMaintainer": ""
	}
```

| Name | Description | Mandatory/Non mandatory | Services |
| --- | --- | --- | --- |
| serviceName | repo name | M | all |
| serviceGroup | group name | M | all |
| repoMaintainer | login whom assign pull request | N | all |
| telegramMaintainer | login Telegram whom assign pull request (ex: @name1 @name2) | N | all |
| branch_from | set argument BRANCH_FROM | N | services_branch_set |
| branch_to | set argument BRANCH_TO | N | services_branch_set |

### Up versions in gradle.properties
Set in file **actual_version.ini**  in format .ini strictly

### Script functionality:
#### [Auto Merge](link)
The configuration variables are described in file [config.py](link/src/auto-merge/config.py)
The location of the service file is specified in the file config.py.

#### [Update Gradle Versions](link/src/upd-gradle-versions)
The configuration variables are described in file [config.py](link/src/upd-gradle-versions/config.py).  
Actual component versions lists in file *actual_version.ini* (**.ini format**), location of the file is specified in config.py.  
upd_gradle_versions runs from the script auto_merge.  

#### [Update Semantic Version](link/src/upd-semantic-version)
The configuration variables are described in file [config.py](link/src/upd-semantic-version/config.py).  
Release version is determined in branch_to.  
upd_gradle_versions runs from the script auto_merge.  

### Auto-move scenario
Consider that the auto-move occurs from branch_from to branch_to:

1. Make changes to files (if required)
   - Upgrading versions in gradle.properties  
   - Remove -SNAPSHOT in gradle.properties  
   - Upgrading versions in semantic-build-versioning.gradle  
2. In branch_from to do a commit with a comment "Pre-Merge Update"  
3. If branch_to is exist, then move to branch_to  
   If branch_to is not exist, then create branch_to and move to it
4. Under branch_to make merge with branch_from with comment "Merge origin/branchA into branchB"  
    * To do merge without fast forward (no_ff)  
5. After all movies run Chech Bot Telegram notifications (about MR, pods, pl)
