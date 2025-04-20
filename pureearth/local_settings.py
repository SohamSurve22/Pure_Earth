
# Local settings for development - Created by local_setup.py
# This file configures the application to use SQLite for local development

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

# Database configuration - SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Set debug to True for development
DEBUG = True

# Set a secret key for development (do not use this in production!)
SECRET_KEY = 'django-insecure-local-development-key-change-in-production'
