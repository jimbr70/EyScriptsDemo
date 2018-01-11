$logspath="c:\qs_scripts_logs.txt"
$junk = New-Item $logspath -type file -force
Add-Content $logspath "==================main-cred.ps1=============V0.1============"

$envVars = (gci env:*).GetEnumerator() | Sort-Object Name | Out-String
Add-Content $logspath $envVars

$script_count=(get-item env:qsscript_count).Value
$script_name = ""
$output=""
$user = (get-item env:qsuname).Value.Trim()
$pass = (get-item env:qspword).Value.Trim()

# if hard set $uname, $pword
#$user = "ET\V9999982"
#$pass = "Chang3M3"

$msg = "Credentials: user {0},  pass {1}" -f $user, $pass
Add-Content $logspath $msg

$execute_command=(get-item env:qsexecute_command).Value

Add-Content $logspath "`nStarting downloads"
    
For ($i=1; $i -le $script_count; $i++) {
    Try {
        $script_name ="qsscript{0}_url" -f $i
        $script_url=(get-item env:$script_name).Value
        $msg= "`nProcessing  {0}"-f $script_url 
        Add-Content $logspath $msg
        
        #Followining is unique to EY's TFS, so far....consistent.
        $fileName = $script_url.Substring($script_url.LastIndexOf("/")+1).Split("&")[0]
        $output="c:\\{0}" -f $fileName
        Add-Content $logspath $output
    
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

Try {
    $msg= "`nExecuting command {0} "-f $execute_command
    Add-Content $logspath $msg

    $ps1,$params = $execute_command.split(" ",2)
    Add-Content $logspath $params
    
    $cmd="c:\\{0}" -f $ps1
    Add-Content $logspath $cmd

    $a = "powershell -file $cmd"
    Add-Content $logspath $a
    
    $invoke_results = (Invoke-Expression "$cmd $params") 2>&1
    if ($lastexitcode) {throw $invoke_results}
    
    Add-Content $logspath "Returned from Invoke-Expression. "
    Add-Content $logspath $invoke_results
    Add-Content $logspath "Script main-cred.ps1 is complete."
}
Catch { 
    $ret_rerr = $_
    $ErrorMessage = $_.Exception.Message
    $FailedItem = $_.Exception.ItemName
    Add-Content $logspath $ret_err
    Add-Content $logspath "ERROR. FAILED execution of script!"
    Add-Content $logspath $ErrorMessage
    Add-Content $logspath $FailedItem
}

#END
