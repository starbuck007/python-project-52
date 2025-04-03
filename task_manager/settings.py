import os
from  pathlib import Path
from dotenv import load_dotenv
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

ROOT_URLCONF = 'task_manager.urls'

WSGI_APPLICATION = 'task_manager.wsgi.application'

INSTALLED_APPS = [
    'task_manager',
    'django.contrib.staticfiles'
]
