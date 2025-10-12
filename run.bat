@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask application...
echo.
echo Access the application at: http://127.0.0.1:5000
echo Admin password: 4129
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
