$script_count=(get-item env:qsscript_count).Value
$script_name = ""
$output=""
$logspath="c:\qs_scripts_logs.txt"

$pname=(get-item env:qspword).Value
$uname=(get-item env:qsuname).Value
$execute_command=(get-item env:qsexecute_command).Value

New-Item $logspath -type file -force
Add-Content $logspath "`nstarts script download"

For ($i=1; $i -le $script_count; $i++) {
    $script_name ="qsscript{0}_url" -f $i
    $script_url=(get-item env:$script_name).Value
    Add-Content $logspath $script_url
    
    $fileName = $script_url.Substring($script_url.LastIndexOf("/")+1)
    $output="c:\\{0}" -f $fileName
    Add-Content $logspath $output
    
    $msg= "`n downloading url : {0}"-f $script_url 
    Add-Content $logspath $msg

    $user = $uname
    $pass = $pname
    Add-Content $logspath $user
    Add-Content $logspath $pass
    
    $securepassword = ConvertTo-SecureString $pass -AsPlainText -Force
    $credentials = New-Object System.Management.Automation.PSCredential($user, $securepassword)
    Invoke-WebRequest -Uri $script_url -Credential $credentials -OutFile $output
}

$msg= "`n  execute command {2} "-f $pname,$uname,$execute_command
Add-Content $logspath $msg

$msg= "`n executing the command {0} "-f $execute_command
Add-Content $logspath $msg

$cmd="c:\\{0}" -f $execute_command

$a = "powershell -file $cmd"
Invoke-Expression $a

#Invoke-Expression(start powershell ($cmd))
#Invoke-Item (start powershell ( $cmd))



