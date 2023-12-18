"""
ASGI config for EventSafari project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventSafari.settings')

#application = get_asgi_application()

import os
import django

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventSafari.settings")
django.setup()
#from apps.ws_routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http":  get_asgi_application(), #AsgiHandler(),#,#AsgiHandler(), 
    # 'websocket':
    #     URLRouter(
    #         websocket_urlpatterns
    #     )
})