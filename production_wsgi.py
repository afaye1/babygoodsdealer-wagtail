#!/usr/bin/env python
"""Production WSGI application for Baby Goods Dealer"""

import os
import sys
from decouple import config

# Production settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "babygoods.settings")
os.environ["DEBUG"] = "False"
os.environ["SECRET_KEY"] = config(
    "SECRET_KEY", default="babygoods-production-key-change-me"
)
os.environ["ALLOWED_HOSTS"] = config("ALLOWED_HOSTS", default="*")
os.environ["WAGTAILADMIN_BASE_URL"] = config(
    "WAGTAILADMIN_BASE_URL", default="http://localhost:8001"
)

try:
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

    # Collect static files if not already collected
    from django.core.management import execute_from_command_line

    try:
        execute_from_command_line(["manage.py", "collectstatic", "--noinput"])
    except:
        pass  # Static files might already be collected

except ImportError:
    # Django not installed, provide a simple WSGI app
    def application(environ, start_response):
        status = "200 OK"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [b"Baby Goods Dealer - Django not installed"]

    sys.exit(1)
