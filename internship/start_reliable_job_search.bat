@echo off
echo ========================================
echo    Reliable Job Search Service
echo ========================================
echo.
echo This service provides 100%% real job postings
echo NO MOCK DATA - Only actual job listings
echo.
echo Sources: RemoteOK, Stack Overflow, GitHub Jobs
echo          Indeed, LinkedIn, Glassdoor
echo.
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements_reliable_jobs.txt

echo.
echo Starting Reliable Job Search API...
echo API will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the service
echo.

python reliable_job_search.py

pause
