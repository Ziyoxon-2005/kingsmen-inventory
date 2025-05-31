@echo off
echo Starting Django Development Server...

REM Create and activate virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Run migrations
python manage.py migrate

REM Start development server
python manage.py runserver 