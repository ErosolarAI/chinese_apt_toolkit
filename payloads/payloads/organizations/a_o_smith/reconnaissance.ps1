
# PowerShell Reconnaissance Payload for A. O. Smith
# Generated: 2025-11-03T11:02:43.730089

function Get-SystemInfo {
    $systemInfo = @{
        Hostname = $env:COMPUTERNAME
        Domain = $env:USERDOMAIN
        Username = $env:USERNAME
        OS = (Get-WmiObject Win32_OperatingSystem).Caption
        Architecture = (Get-WmiObject Win32_OperatingSystem).OSArchitecture
        IPAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq "Ethernet" -or $_.InterfaceAlias -eq "Wi-Fi"}).IPAddress
        MACAddress = (Get-NetAdapter | Where-Object {$_.Status -eq "Up"}).MacAddress
    }
    return $systemInfo
}

function Get-NetworkShares {
    return Get-SmbShare | Select-Object Name, Path, Description
}

function Get-InstalledSoftware {
    return Get-WmiObject -Class Win32_Product | Select-Object Name, Version, Vendor
}

# Execute reconnaissance
$reconData = @{
    SystemInfo = Get-SystemInfo
    NetworkShares = Get-NetworkShares
    InstalledSoftware = Get-InstalledSoftware
}

# Convert to JSON and save to temp file
$reconData | ConvertTo-Json -Depth 3 | Out-File "$env:TEMP\a_o_smith_recon.json"

Write-Host "Reconnaissance completed for A. O. Smith"
