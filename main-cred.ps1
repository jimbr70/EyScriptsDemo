New-Item $logspath -type file -force
$logspath="c:\qs_scripts_logs.txt"
Add-Content $logspath "==================main-cred.ps1=============V0.0============"

$envVars = (gci env:*).GetEnumerator() | Sort-Object Name | Out-String
Add-Content $logspath $envVars

$script_count=(get-item env:qsscript_count).Value
$script_name = ""
$output=""
$user = (get-item env:qsuname).Value.Trim()
$pass = (get-item env:qspword).Value.Trim()

# if hard set $uname, $pword
$hc_user = "ET\V9999982"
$hc_pass = "Chang3M3"

$msg = "u--{0}--{1}--" -f $user, $hc_user
Add-Content $logspath $msg
$msg = "p--{0}--{1}--" -f $pass, $hc_pass
Add-Content $logspath $msg

if ($user -eq $hc_user) {
   Add-Content $logspath "users equal"
   }
if ($pass -eq $hc_pass) {
   Add-Content $logspath "passwords equal"
   }
$msg = "user {0},  pass {1}" -f $user, $pass
Add-Content $logspath $msg

$execute_command=(get-item env:qsexecute_command).Value

Add-Content $logspath "`nStarting downloads"
    
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

$msg= "`nExecuting command {0} "-f $execute_command
Add-Content $logspath $msg

$cmd="c:\\{0}" -f $execute_command

$a = "powershell -file $cmd"
Invoke-Expression $a

Add-Content $logspath "Returned from Invoke-Expression.  Script main-cred.ps1 is complete."

#END
