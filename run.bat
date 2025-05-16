@echo off
echo ==========================================
echo      Syntax Motion - Development Mode
echo ==========================================
echo.

:: Check prerequisites
echo Checking prerequisites...

:: Check Python
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo Error: Python is not installed. Please install Python 3.10 or higher.
  exit /b 1
)
echo Python installed.

:: Check Node.js
node --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo Error: Node.js is not installed. Please install Node.js 18 or higher.
  exit /b 1
)
echo Node.js installed.

:: Check npm
npm --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo Error: npm is not installed. Please install npm.
  exit /b 1
)
echo npm installed.

:: Check PostgreSQL (not a hard requirement, just a warning)
where psql >NUL 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo Warning: PostgreSQL CLI (psql) is not found. Make sure PostgreSQL is running.
) else (
  echo PostgreSQL CLI installed.
)

:: Check if Manim is installed
python -c "import manim" 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo Warning: Manim is not installed in the current Python environment.
  echo This may be ok if you're using a virtual environment for the backend.
) else (
  echo Manim installed.
)

echo.
echo Starting Backend and Frontend Services...
echo.

:: Start backend
echo Starting backend server...
if exist backend\.venv (
  echo Activating virtual environment...
  call backend\.venv\Scripts\activate
) else (
  echo Warning: No virtual environment found at backend\.venv
  echo Using system Python. It's recommended to create a virtual environment.
)

cd backend
if not exist .env (
  echo Warning: No .env file found in backend directory.
  echo Creating .env from .env.example...
  copy .env.example .env
  echo Please update the .env file with your database and API credentials.
)

echo Installing backend dependencies...
pip install -r requirements.txt

echo Starting backend server...
start "Syntax Motion Backend" cmd /k python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo Backend server started!
echo Backend available at: http://localhost:8000

:: Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > NUL
cd ..

:: Start frontend
echo Starting frontend server...
cd frontend
echo Installing frontend dependencies...
call npm install

echo Starting frontend development server...
start "Syntax Motion Frontend" cmd /k npm run dev
echo Frontend server started!
echo.

echo ==========================================
echo    All services started successfully!
echo ==========================================
echo.
echo Frontend URL: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the command windows to stop the services.
echo.

:: Wait for user input before exiting
pause 