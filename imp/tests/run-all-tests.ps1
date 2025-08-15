Write-Output "🚀 Running Full Cimp System Test Suite..."
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
python "$PSScriptRoot\run_all_tests.py"
