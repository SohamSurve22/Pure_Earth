#!/usr/bin/env python
"""
Django development server starter.
"""
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define the app for Gunicorn
from pureearth.wsgi import application
app = application

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pureearth.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    
    # Start development server
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5000'])
