# Task Manager
[![Actions Status](https://github.com/starbuck007/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/starbuck007/python-project-52/actions)
[![Python CI](https://github.com/starbuck007/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/starbuck007/python-project-52/actions/workflows/pyci.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=starbuck007_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=starbuck007_python-project-52)

A web application for task management built with Django. This project enables teams to organize their work by creating and tracking tasks, assigning executors, setting statuses, and adding labels.

Demo: https://task-manager-9vul.onrender.com/

## Features

- User authentication and authorization
- Task creation and management
- Status tracking
- Labeling system
- Task filtering by various parameters
- Error tracking with Rollbar

## Requirements

- Python 3.10 or higher
- Django - Web framework
- python-dotenv - Environment variable management
- dj-database-url - Database URL configuration
- gunicorn - WSGI HTTP server
- psycopg2-binary - PostgreSQL adapter
- django-bootstrap5 - Bootstrap 5 integration
- coverage - Test coverage measurement
- rollbar - Error tracking service

## Installation
```commandline
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

## Environment setup
Create a `.env` file in the project root:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # Or your PostgreSQL connection
ROLLBAR_ACCESS_TOKEN=your_rollbar_token
ROLLBAR_ENABLED=True
```

## Usage

### Using Makefile commands

```commandline
# Install dependencies
make install

# Collect static files
make collectstatic

# Apply migrations
make migrate

# Run the development server
make run

# Run tests
make test

# Generate coverage report
make cov

# Build for deployment
make build

# Start with gunicorn (for production)
make render-start
```
Visit http://localhost:8000

## Deployment

This application can be deployed to Render.
