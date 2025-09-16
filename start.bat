@echo off
echo Starting E-Commerce Django Application...
echo ==========================================

echo.
echo Checking if server is already running...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Warning: Python processes are already running. You may need to close existing servers.
    echo.
)

echo Starting Django development server...
echo.
echo Your E-Commerce Application will be available at:
echo  -> Homepage: http://127.0.0.1:8000/
echo  -> Admin Panel: http://127.0.0.1:8000/admin/
echo  -> Products: http://127.0.0.1:8000/products/
echo.
echo Admin Login Credentials:
echo  -> Username: admin
echo  -> Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python manage.py runserver