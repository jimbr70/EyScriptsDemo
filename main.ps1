$script1=(get-item env:qsscript1_url).Value
$script2=(get-item env:qsscript2_url).Value
$script3=(get-item env:qsscript3_url).Value


Invoke-WebRequest -Uri $script1 -OutFile "c:\\downloadme1.txt"
Invoke-WebRequest -Uri $script2 -OutFile "c:\\downloadme2.txt"
Invoke-WebRequest -Uri $script2 -OutFile "c:\\downloadme3.txt"

#$url ="https://raw.githubusercontent.com/QualiSystems/EyScriptsDemo/master/downloadme1.txt"
#$output = "$PSScriptRoot\downloadme1.txt"
#$output2 = "c:\\downloadme1.txt"
#Invoke-WebRequest -Uri $url -OutFile $output2


