## upd_gradle_versions

This script update **gradle.properties** file  

![The Gradle](images/gradle.png)

##### Functional:
1. The script remove **-SNAPSHOT**, if '--rm_snapshot' parameter is 'True'.
2. The script update versions of services, if version of service in actual_version.ini file higher, than in gradle.properties.  
   **actual_version.ini** must contain actual version of services.  
   **actual_version.ini** location is defined in **config.py**.
   

##### To run script: 

> main.py --branch_to=[branch] --rm_snapshot=True


##### Parameters:  
`--branch_to/-b - branch to change (ex: test10, develop11, release15)`  
`--up_version/-u - can be True/False. Default: False`
`--remove_snapshot/-r - can be True/False. Default: False`  
`--help/-h - info about parameters`

