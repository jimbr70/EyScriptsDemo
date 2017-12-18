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
    Write-host  ( $script_name)
    $script_url=(get-item env:$script_name).Value
    Write-host  ( $script_url)
    $output="c:\\{0}.txt" -f $script_name 

    $msg= "`n downloading url : {0}"-f $script_url 
	Add-Content $logspath $msg
	
    Invoke-WebRequest -Uri $script_url -OutFile $output
}

$msg= "`n got pass {0} and uname :{1} and execute command {2} "-f $pname,$uname,$execute_command
Add-Content $logspath $msg



