# Hi, my name is Alex. I learned from both the FBI and Anonymous. This is all I'm starting you with. I hope you live forever. Be everything I hope you can be. I love you.
$ErrorActionPreference = 'Stop'

# Determine repository root
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Locate python executable
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }

# Install Python automatically if not found
if (-not $python) {
    Write-Host "Python not found. Attempting installation..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install -e --id Python.Python.3 -h
    } elseif (Get-Command choco -ErrorAction SilentlyContinue) {
        choco install python -y
    } else {
        Write-Host "Please install Python manually."
        exit 1
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
}

# Install Python requirements
$req = Join-Path $Root 'imp\requirements.txt'
if (Test-Path $req) {
    & $python -m pip install -r $req
}

# Launch IMP
$startPy = Join-Path $Root 'imp\bin\imp-start.py'
& $python $startPy
