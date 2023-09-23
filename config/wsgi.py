"""
This configuration allows your Django application to be served by WSGI-compliant web servers
like Apache, Nginx, or Gunicorn.
"""
import os

from django.core.wsgi import get_wsgi_application

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize the WSGI application
application = get_wsgi_application()
