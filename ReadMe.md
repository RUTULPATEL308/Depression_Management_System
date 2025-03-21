# How to Run the Depression Management System

## Prerequisites
Ensure you have the following installed on your system:
- Python (>=3.8)
- PostgreSQL
- Git
- Virtualenv (Optional but recommended)
- Node.js & npm (if the project has frontend dependencies)

## Clone the Repository
```bash
git clone -b Feature https://github.com/RUTULPATEL308/Depression_Management_System.git
cd Depression_Management_System
```

## Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Database Setup
1. Start PostgreSQL and create a database:
```sql
CREATE DATABASE depression_management;
```
2. Update the `.env` file with your database credentials:
```
DB_NAME=depression_management
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Create a Superuser (Optional, for Admin Panel Access)
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a superuser.

## Run the Server
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

## Running Tests (Optional)
To ensure everything is working correctly, run:
```bash
python manage.py test
```

## API Endpoints (If Applicable)
- `POST /api/mood-detection/` - Submit user data for mood analysis
- `GET /api/suggestions/` - Retrieve AI-generated suggestions

## Frontend (If Applicable)
If the project has a frontend, navigate to the frontend directory and start the application:
```bash
python manage.py runserver
```
The frontend will be available at `http://127.0.0.1:8000/`.

## Deployment (Optional)
For deployment, consider using:
- **Docker:** Create a `Dockerfile` and use `docker-compose`.
- **Heroku/AWS/Azure:** Set up environment variables and push the project.

---
Now your Depression Management System should be up and running! 🚀

