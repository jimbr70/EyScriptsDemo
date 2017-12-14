$script_count=(get-item env:qsscript_count).Value
$script_name = ""
$output=""
$pname=(get-item env:qspname).Value
$uname=(get-item env:qsuname).Value

For ($i=1; $i -le $script_count; $i++) {
    $script_name ="qsscript{0}_url" -f $i

    Write-host  ( $script_name)
    $script_url=(get-item env:$script_name).Value
    Write-host  ( $script_url)
    $output="c:\\{0}.txt" -f $script_name 
    Invoke-WebRequest -Uri $script_url -OutFile $output
}



