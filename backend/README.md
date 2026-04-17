# Backend

Flask backend for the Library Management System.

## Contents

- app.py: main Flask app and API routes
- celery_jobs/tasks.py: Celery tasks
- celery_jobs/app_factory.py: Celery app factory helper
- celery_jobs/context_task.py: Flask context task wrapper
- celery_jobs/config.py: Redis broker/result settings
- celery_jobs/celerybeat-schedule: Celery beat schedule file
- config.py: Flask config
- utils/: utility modules
- instance/: SQLite DB and stored files

## Run Locally

1. Create and activate virtual environment.
2. Install packages:

   pip install -r requirements.txt

3. Start API:

   python app.py

## Optional: Celery Worker

Run from backend folder:

celery -A tasks.celery_app worker --loglevel=info
