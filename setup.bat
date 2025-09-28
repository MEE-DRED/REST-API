@echo off
echo ========================================
echo SMS Transactions REST API Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    echo Alternative: If Python is installed, try:
    echo   py --version
    echo   or check your PATH environment variable
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

echo.
echo Checking project structure...

if not exist "api\server.py" (
    echo ❌ API server file not found
    echo Make sure you're in the correct directory: %CD%
    echo Expected location: %CD%\api\server.py
    pause
    exit /b 1
)

if not exist "data\modified_sms_v2.xml" (
    echo ❌ XML data file not found
    echo Make sure all project files are present
    echo Expected location: %CD%\data\modified_sms_v2.xml
    pause
    exit /b 1
)

if not exist "dsa\xml_parser.py" (
    echo ❌ DSA module file not found
    echo Expected location: %CD%\dsa\xml_parser.py
    pause
    exit /b 1
)

echo ✅ Project structure looks good

echo.
echo Checking Python modules...

echo Checking standard library modules...
python -c "import json, xml.etree.ElementTree, base64, urllib.parse, time" >nul 2>&1
if errorlevel 1 (
    echo ❌ Standard library modules missing (this shouldn't happen)
    pause
    exit /b 1
) else (
    echo ✅ Standard library modules available
)

echo.
echo Checking optional dependencies...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  'requests' module not found
    echo Installing requests for testing...
    pip install requests
    if errorlevel 1 (
        echo ❌ Failed to install requests
        echo You can still run the API server, but automated testing won't work
        echo Try manually: pip install requests
    ) else (
        echo ✅ requests installed successfully
    )
) else (
    echo ✅ requests module is available
)

echo.
echo Testing project components...
python verify_project.py
if errorlevel 1 (
    echo ⚠️  Some components had issues
    echo Check the output above for details
) else (
    echo ✅ All components verified successfully
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo What to do next:
echo.
echo 1. Start the API server:
echo    python api\server.py
echo.
echo 2. Test the API (in another terminal):
echo    python api\test_api.py
echo    OR
echo    test_api_curl.bat
echo.
echo 3. Read the documentation:
echo    docs\api_docs.md
echo.
echo 4. Check the README:
echo    README.md
echo.
echo The API will run on: http://localhost:8000
echo.
echo Valid credentials:
echo - admin:password123
echo - user:user123  
echo - demo:demo123
echo.
pause