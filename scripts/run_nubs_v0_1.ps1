# ==============================================================================
# NUBS Deployment and Execution Script v0.1
# Purpose: Automate environment setup and launch the NUBS Dashboard
# Usage: .\scripts\run_nubs_v0_1.ps1
# ==============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  NUBS (Normal Users Bridge-Switch) Deployment Script v0.1" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Check Python installation
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = python --version
Write-Host "[INFO] Found $pythonVersion" -ForegroundColor Green

# 2. Setup Virtual Environment (if not exists)
$venvPath = ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "[INFO] Creating isolated virtual environment at $venvPath..." -ForegroundColor Yellow
    python -m venv $venvPath
} else {
    Write-Host "[INFO] Virtual environment already exists." -ForegroundColor Green
}

# 3. Activate Virtual Environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"

# 4. Install/Update Dependencies
Write-Host "[INFO] Ensuring dependencies are installed from requirements.txt..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# 5. Launch Dashboard
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Starting NUBS Dashboard..." -ForegroundColor Green
Write-Host "  Access it in your browser at: http://localhost:8501" -ForegroundColor Green
Write-Host "  Press Ctrl+C in this window to stop the server." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

streamlit run src/ui/dashboard_app_v0_1.py