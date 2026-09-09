param(
    [Parameter(Mandatory=$true)][ValidatePattern('^[a-zA-Z0-9_-]+$')][string]$BusinessId,
    [ValidateRange(1024,65535)][int]$ApiPort = 8790,
    [ValidateRange(1024,65535)][int]$DashboardPort = 3000
)
$ErrorActionPreference = 'Stop'
$repoPath = Split-Path $PSScriptRoot -Parent
$pythonPath = Join-Path $repoPath '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { throw 'Install requirements-runtime.txt in .venv first.' }
if (-not (Test-Path -LiteralPath (Join-Path $repoPath 'dashboard\.next\BUILD_ID'))) { throw 'Run npm ci and npm run build in dashboard first.' }
if ($ApiPort -eq $DashboardPort) { throw 'API and dashboard ports must differ.' }
foreach ($port in @($ApiPort, $DashboardPort)) {
    $probe = [System.Net.Sockets.TcpClient]::new()
    try { $probe.Connect('127.0.0.1', $port); throw "Port $port is occupied; stop the existing service or select another port." }
    catch [System.Net.Sockets.SocketException] { }
    finally { $probe.Dispose() }
}
$privatePath = Join-Path $repoPath 'instance\private'
New-Item -ItemType Directory -Path $privatePath -Force | Out-Null
$secretPath = Join-Path $privatePath 'runtime-credentials.clixml'
if (-not (Test-Path -LiteralPath $secretPath)) {
    $secretRecords = @{}
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        foreach ($role in @('owner','reviewer','worker')) {
            $bytes = New-Object byte[] 32
            $rng.GetBytes($bytes)
            $secretRecords[$role] = ConvertTo-SecureString ([Convert]::ToBase64String($bytes)) -AsPlainText -Force
        }
        $secretRecords | Export-Clixml -LiteralPath $secretPath
    } finally { $rng.Dispose() }
}
# Export-Clixml encrypts SecureString values with Windows DPAPI for this user.
$secrets = Import-Clixml -LiteralPath $secretPath
$previousEnvironment = @{}
$settings = @{
    BUSINESSOS_INSTANCE_ID = $BusinessId
    BUSINESSOS_DATA_DIR = (Join-Path $repoPath 'instance\runtime')
    BUSINESSOS_API_URL = "http://127.0.0.1:$ApiPort"
    BUSINESSOS_PUBLIC_ORIGIN = "http://127.0.0.1:$DashboardPort"
    BUSINESSOS_MODE = 'live'
    HOSTNAME = '127.0.0.1'
    PORT = "$DashboardPort"
}
foreach ($role in @('owner','reviewer','worker')) {
    $settings['BUSINESSOS_' + $role.ToUpperInvariant() + '_TOKEN'] = [System.Net.NetworkCredential]::new('', $secrets[$role]).Password
}
foreach ($key in $settings.Keys) {
    $previousEnvironment[$key] = [Environment]::GetEnvironmentVariable($key, 'Process')
    [Environment]::SetEnvironmentVariable($key, $settings[$key], 'Process')
}
$runtimeProcess = $null
Push-Location (Join-Path $repoPath 'dashboard')
try {
    $runtimeProcess = Start-Process -FilePath $pythonPath -ArgumentList @('-m','businessos','serve','--port',"$ApiPort") -WorkingDirectory $repoPath -WindowStyle Hidden -PassThru
    $healthy = $false
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        if ($runtimeProcess.HasExited) { throw 'Runtime exited during startup.' }
        try {
            $health = Invoke-RestMethod -Uri "http://127.0.0.1:$ApiPort/healthz" -TimeoutSec 1
            if ($health.service -eq 'businessos-runtime' -and $health.business_id -eq $BusinessId) { $healthy = $true; break }
        } catch { }
        Start-Sleep -Milliseconds 250
    }
    if (-not $healthy) { throw 'Runtime did not become healthy.' }
    Write-Host "Open http://127.0.0.1:$DashboardPort . Credentials are encrypted in instance/private/runtime-credentials.clixml. See the runtime guide for login."
    & npm.cmd start
    if ($LASTEXITCODE -ne 0) { throw 'Dashboard exited with an error.' }
} finally {
    if ($null -ne $runtimeProcess -and -not $runtimeProcess.HasExited) { Stop-Process -Id $runtimeProcess.Id }
    Pop-Location
    foreach ($key in $previousEnvironment.Keys) { [Environment]::SetEnvironmentVariable($key, $previousEnvironment[$key], 'Process') }
}
