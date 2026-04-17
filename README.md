# LibraryManagementSystem_VueJS

This repository is organized into clear frontend and backend areas.

## Project Structure

- backend: Flask API, Celery tasks, backend configs, database instance, and Python requirements.
- frontend: Vue.js application.
- docs: project documentation and reports.
- scripts: helper scripts for local development.
- tests: placeholder for automated tests.

## Quick Start

### 1) Backend

1. Open terminal in backend folder.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Run backend server:

   python app.py

### 2) Frontend

1. Open terminal in frontend folder.
2. Install dependencies:

   npm install

3. Start dev server:

   npm run serve

## Notes

- SQLite database and uploaded files are under backend/instance.
- Celery and Redis settings are in backend/CeleryConfig.py.
- Legacy dependency file is kept as backend/requirements-legacy.txt.
