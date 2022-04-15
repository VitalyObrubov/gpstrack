"""
ASGI config for gpstrack project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from websocket.middleware import websockets

if os.environ.get('DJANGO_SETTINGS_MODULE') == None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpstrack.settings')

application = get_asgi_application()
application = websockets(application)
