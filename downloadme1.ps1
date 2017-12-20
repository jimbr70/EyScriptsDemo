param([Int32]$data)
$logspath="c:\qs_scripts_logs_test_run{0}.txt" -f $data
New-Item $logspath -type file -force
Add-Content $logspath "`nstarts script download"
Add-Content $logspath  $data

#$logspath="c:\qs_scripts_logs_test_run.txt"
#New-Item $logspath -type file -force
#Add-Content $logspath "`nstarts script download"
