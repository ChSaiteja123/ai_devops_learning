$ErrorActionPreference = "Stop"

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

$pythonExe = Join-Path $projectPath "sai\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Python environment not found at $pythonExe. Create the virtual environment first."
    exit 1
}

Write-Host "Starting DevOps Learning Platform..."
& $pythonExe manage.py migrate
& $pythonExe manage.py runserver 0.0.0.0:8000
