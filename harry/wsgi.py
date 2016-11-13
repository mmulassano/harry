"""
WSGI config for harry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/var/www/html')
sys.path.append('/var/www/html/harryapp')
sys.path.append('/var/www/html/harryapp/media/')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "harry.settings")

application = get_wsgi_application()
