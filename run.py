"""
This script runs the PureEarth Django application.
It attempts to use Gunicorn if available, otherwise falls back to Django's development server.
"""
import os
import sys
import subprocess
import importlib.util

def is_package_installed(package_name):
    """Check if a package is installed."""
    return importlib.util.find_spec(package_name) is not None

if __name__ == "__main__":
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pureearth.settings')
    
    # Default port (can be overridden with environment variable)
    port = os.environ.get('PORT', '8000')
    host = "0.0.0.0"
    
    try:
        # First try to run with Gunicorn if installed
        if is_package_installed('gunicorn'):
            print(f"Starting PureEarth with Gunicorn on http://{host}:{port}")
            subprocess.check_call([
                "gunicorn",
                "--bind", f"{host}:{port}",
                "--reload",
                "pureearth.wsgi:application"
            ])
        else:
            # Fall back to Django's development server
            print(f"Gunicorn not found, starting with Django development server on http://{host}:{port}")
            print("Note: For production use, install Gunicorn with: pip install gunicorn")
            
            # Import Django management
            try:
                from django.core.management import execute_from_command_line
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import Django. Are you sure it's installed?"
                ) from exc
            
            # Start development server
            execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])
    
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
