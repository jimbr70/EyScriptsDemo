$logspath="c:\qs_scripts_logs.txt"
Add-Content $logspath "======================================================="

$envvars = gci env:* | sort-object name
Add-Content $logspath $envvars

$script_count=(get-item env:qsscript_count).Value
$script_name = ""
$output=""

$pword=(get-item env:qspword).Value
$uname=(get-item env:qsuname).Value
$execute_command=(get-item env:qsexecute_command).Value

New-Item $logspath -type file -force
Add-Content $logspath "`nStart script download"

# hard was $uname, $pword
$user = "ET\V9999982"
$pass = "Chang3M3"
$msg = "user {0},  pass {1}" -f $user, $pass
Add-Content $logspath $msg
    
For ($i=1; $i -le $script_count; $i++) {
    Try {
    $script_name ="qsscript{0}_url" -f $i
    $script_url=(get-item env:$script_name).Value
    Add-Content $logspath $script_url
    
    $fileName = $script_url.Substring($script_url.LastIndexOf("/")+1).Split("&")[0]
    $output="c:\\{0}" -f $fileName
    Add-Content $logspath $output
    
    $msg= "`nDownloading  {0}"-f $script_url 
    Add-Content $logspath $msg

    $securepassword = ConvertTo-SecureString $pass -AsPlainText -Force
    $credentials = New-Object System.Management.Automation.PSCredential($user, $securepassword)
    Invoke-WebRequest -Uri $script_url -Credential $credentials -OutFile $output
    }
    Catch {
    $ErrorMessage = $_.Exception.Message
    $FailedItem = $_.Exception.ItemName
    Add-Content $logspath $ErrorMessage
    Add-Content $logspath $FailedItem
    }
    Add-Content $logspath "-----------------------------------------------"
}

$msg= "`n executing the command {0} "-f $execute_command
Add-Content $logspath $msg

$cmd="c:\\{0}" -f $execute_command

$a = "powershell -file $cmd"
Invoke-Expression $a

Add-Content $logspath "Returned from command. Script Complete."

#END
