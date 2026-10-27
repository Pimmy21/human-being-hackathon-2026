param(
    [string]$Python = '.venv/Scripts/python.exe',
    [string]$EnvFile = '.env.local',
    [string]$HMemReference = '',
    [string]$State = 'purrpose/.state/hmem',
    [string]$Workspace = 'purrpose-demo',
    [int]$Port = 8767,
    [switch]$EnableZetaris,
    [string]$JdbcPython = '',
    [string]$Jvm = ''
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $repoRoot
try {
    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw 'Python not found. Create .venv or pass -Python.' }
    if (-not (Test-Path -LiteralPath $EnvFile -PathType Leaf)) { throw 'Copy .env.example to .env.local and configure your tools first.' }
    $launchArgs = @('-u', '-m', 'purrpose.server', '--port', "$Port", '--env-file', $EnvFile)
    if ($HMemReference) {
        if (-not (Test-Path -LiteralPath $HMemReference -PathType Leaf)) { throw 'H-MEM reference index.ts not found.' }
        $launchArgs += @('--reference', $HMemReference, '--state', $State, '--workspace', $Workspace)
    }
    if ($EnableZetaris) {
        if (-not $JdbcPython) { $JdbcPython = $Python }
        if (-not (Test-Path -LiteralPath $JdbcPython -PathType Leaf)) { throw 'JDBC Python not found.' }
        if (-not $Jvm -or -not (Test-Path -LiteralPath $Jvm -PathType Leaf)) { throw 'Pass -Jvm with your existing jvm.dll, libjvm.so or libjvm.dylib path.' }
        $launchArgs += @('--zetaris-remote-env', $EnvFile, '--zetaris-python', $JdbcPython, '--zetaris-jvm', $Jvm)
    }
    & $Python @launchArgs
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
