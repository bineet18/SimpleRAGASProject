@echo off
:: Quick virtual environment setup for Windows
:: Usage: quickstart.bat

:: Check if venv exists, create if not
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
venv\Scripts\activate


echo Virtual environment activated.
echo Python: %CD%\venv\Scripts\python.exe
echo Run 'deactivate' to exit.