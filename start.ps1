# Greyskull Workout Tracker - Quick Start Script
# Run this script to set up and start your app

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Greyskull Workout Tracker - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠ .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Edit .env file and change these settings:" -ForegroundColor Yellow
    Write-Host "  - SECRET_KEY (set to something random)" -ForegroundColor White
    Write-Host "  - AUTH_PASSWORD (set your password)" -ForegroundColor White
    Write-Host "  - FLASK_DEBUG (set to False for production)" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "Press Enter when you've edited .env, or 'skip' to continue anyway"
    if ($continue -ne "skip") {
        Write-Host "Opening .env file..." -ForegroundColor Yellow
        notepad .env
        Read-Host "Press Enter when done editing"
    }
}

Write-Host ""

# Install dependencies
Write-Host "Installing Python packages..." -ForegroundColor Yellow
Write-Host "(This may take a minute)" -ForegroundColor Gray
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Try running manually: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! Starting app..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access your app at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the app
python app.py
