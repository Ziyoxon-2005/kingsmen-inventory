@echo off
echo Setting up Django Inventory Management System for Windows...

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.9 or later.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    echo DEBUG=True > .env
    echo DJANGO_SECRET_KEY=local-dev-key >> .env
    echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env
    echo DATABASE_URL=sqlite:///db.sqlite3 >> .env
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser if it doesn't exist
echo Checking for superuser...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None"

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo Setup complete! You can now run the development server using:
echo start.bat
echo Or run with Docker using:
echo docker-start.bat 