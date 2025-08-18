Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Reliable Job Search Service" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This service provides 100% real job postings" -ForegroundColor Green
Write-Host "NO MOCK DATA - Only actual job listings" -ForegroundColor Green
Write-Host ""
Write-Host "Sources: RemoteOK, Stack Overflow, GitHub Jobs" -ForegroundColor Yellow
Write-Host "         Indeed, LinkedIn, Glassdoor" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements_reliable_jobs.txt

Write-Host ""
Write-Host "Starting Reliable Job Search API..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the service" -ForegroundColor Yellow
Write-Host ""

python reliable_job_search.py

Read-Host "Press Enter to exit"
