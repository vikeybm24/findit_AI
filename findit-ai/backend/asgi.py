# File: backend/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# This is the main entry point for ASGI.
# It will first handle standard HTTP requests.
# Later, we will add WebSocket routing here.
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": ... We will add this in the next step
})