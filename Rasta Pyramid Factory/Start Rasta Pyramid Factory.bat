@echo off
setlocal
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1

where pyw >nul 2>nul
if %errorlevel%==0 (
  start "" pyw -3.14 "START RASTA PYRAMID FACTORY.pyw"
  exit /b 0
)

where pythonw >nul 2>nul
if %errorlevel%==0 (
  start "" pythonw "START RASTA PYRAMID FACTORY.pyw"
  exit /b 0
)

echo Python 3.14 GUI launcher was not found.
echo Install Python 3.14.5, then try again.
pause
endlocal
