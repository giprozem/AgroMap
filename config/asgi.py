"""
asgi.py is a Python script used in Django web applications to provide an ASGI (Asynchronous Server Gateway Interface) entry point for handling asynchronous web requests.
ASGI is a specification that allows Django to handle asynchronous operations such as WebSockets, long-polling, and other real-time functionality in addition to traditional
synchronous HTTP requests.
"""

#Import Statements
import os

from django.core.asgi import get_asgi_application

#Environment Configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

#ASGI Application Initialization
application = get_asgi_application()
