# voMMXS1Ip5rAnxxBv37s
# Generated: 2025-11-03T12:20:52.710479
# System: Tu6Kf4fyuzj3ngc
# Process: 2QZvK0TnnoEN


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
