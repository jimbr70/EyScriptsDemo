#!/bin/bash
cd /tmp
mkdir csd
cd /tmp/csd

curl https://raw.githubusercontent.com/jimbr70/EyScriptsDemo/master/linux_deploy.py -o linux_deploy.py

#curl --ntlm --user 'L.CMFCS.01:JjFjtX!#E+D8w63Q' 'http://10.254.34.24:8080/tfs/DefaultCollection/d3782bb2-7bbf-48fd-8f3a-0b7e24507bac/_api/_versioncontrol/itemContent?repositoryId=78d6293c-71cd-4c07-8e3e-6f85e30e6144&path=/sccm/Deploy-SCCMClient.ps1&version=GBmaster&contentOnly=false&__v=5' -o bla.py

python ./linux_deploy.py

