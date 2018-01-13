#Secure log file name   <hostname>_<source>_yyyy-mm-dd-HH-mm-ss.log
Try {
    $logspath = "C:\\{0}" -f $(hostname)
    $logspath += "_main-cred_" + $(get-date -f yyyy-MM-dd-HH-mm-ss) + ".log"
    $junk = New-Item $logspath -type file -force
} Catch {
    $logspath="c:\qsapps_main-cred.txt"
    $junk = New-Item $logspath -type file -force
    Add-Content $logspath "ERROR in setting up proper logfile name; using default."
}

Add-Content $logspath "main-cred.ps1=====V0.1======" + $(get-date -f yyyy-MM-dd-HH-mm-ss)

$envVars = (gci env:*).GetEnumerator() | Sort-Object Name | Out-String
Add-Content $logspath $envVars

$script_count=(get-item env:qsscript_count).Value
$script_name = ""
$output=""
$user = (get-item env:qsuname).Value.Trim()
$pass = (get-item env:qspword).Value.Trim()

#$msg = "Credentials: user {0},  pass {1}" -f $user, $pass
#Add-Content $logspath $msg

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
    $execute_command=(get-item env:qsexecute_command).Value

    $msg= "`nExecuting command {0} "-f $execute_command
    Add-Content $logspath $msg

    $ps1,$params = $execute_command.split(" ",2)
    #Add-Content $logspath $params
    
    $cmd="c:\\{0}" -f $ps1
    #Add-Content $logspath $cmd

    $invoke_results = (Invoke-Expression "$cmd $params") 2>&1
    if ($lastexitcode) {throw $invoke_results}
    
    Add-Content $logspath "Returned from Invoke-Expression. "
    Add-Content $logspath $invoke_results
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

# FTP Log Phase
Add-Content $logspath "Done.  Putting log on ftp server"
$rsvnID = (get-item env:reservation_id).Value.Trim()
$ftpsrvr = (get-item env:ftpsrvr).Value.Trim()
$ftpuser = (get-item env:ftpuser).Value.Trim()
$ftppass = (get-item env:ftppass).Value.Trim()

#Create meta-data file for EY scripts to leverage
$metadata = "C:\rsvn-meta-data.txt"
$junk = New-Item $metadata -type file -force
$mdata = "rsvnId: $rsvnID`r`n"
$mdata += "ftp_srvr: $ftpsrvr`r`n"
$mdata += "ftp_user: $ftpuser`r`n"
$mdata += "ftp_pass: $ftppass`r`n"
Add-Content $metadata $mdata

# psftp in batch mode (-b) avoids prompt regarding server certificate
Try {
    $ftp_commands = "C:\\ftp_commands.cmd"
    $junk = New-Item $ftp_commands -type file -force
    Add-Content $ftp_commands "cd Logs"
    Add-Content $ftp_commands "dir"
    Add-Content $ftp_commands "quit"
    Add-Content $logspath "exec listing"
    $listing = C:\\psftp -l $ftpuser -pw $ftppass -b "C:\\ftp_commands.cmd" $ftpsrvr
    Add-Content $logspath "first done"
    Remove-Item $ftp_commands
    Add-Content $logspath "first removed"
    
    $junk = New-Item $ftp_commands -type file -force
    Add-Content $ftp_commands "cd Logs"
    Add-Content $ftp_commands "dir"

    Add-Content $logspath "pre if exists"
    if ($listing -like "*" + $rsvnID + "*") {
	    Add-Content $ftp_commands "mkdir $rsvnID"
        }
    Add-Content $logspath "post if exists"
    Add-Content $ftp_commands "cd $rsvnID"
    Add-Content $ftp_commands 'lcd C:\'
    Add-Content $ftp_commands "put $logspath"
    Add-Content $ftp_commands "quit"
    
    $put_result = C:\psftp -l $ftpuser -pw $ftppass -b "C:\\ftp_commands.cmd" $ftpsrvr
    Remove-Item $ftp_commands
} Catch {
    $ErrorMessage = $_.Exception.Message
    $FailedItem = $_.Exception.ItemName
    Add-Content $logspath "ERROR in ftp section"
    Add-Content $logspath $ErrorMessage
    Add-Content $logspath $FailedItem
}

Add-Content $logspath "Script main-cred.ps1 is complete."

#END
