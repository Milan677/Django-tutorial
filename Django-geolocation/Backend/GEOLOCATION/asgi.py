"""
ASGI config for GEOLOCATION project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GEOLOCATION.settings')

# application = get_asgi_application()


# project_name/asgi.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GEOLOCATION.settings")

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import channelapp.routing

django.setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            channelapp.routing.websocket_urlpatterns
        )
    ),
})

