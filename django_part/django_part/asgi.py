"""
ASGI config for django_part project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

from WSSGTemplate.NetworkAnalyser import NetworkAnalyser
from WSSGTemplate.websocket_scripts.routing import websocket_urlpatterns
from django_part import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_part.settings')
django_asgi_app = get_asgi_application()
django_wsgi_app = get_wsgi_application()


# custom middleware to get more information about all requests
class PrintHttpRequestMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        print(scope)
        if scope['type'] == 'http':
            # If it's an HTTP request, print information about the request
            print(f"Received HTTP request for path: {scope['path']}")

        # print(f"scope:\n{scope}")

        async def receive_wrapper():
            net = NetworkAnalyser()
            net.record_request()
            # print(f"Ingoing Reqeust Content {receive}")
            return await receive()

        async def send_wrapper(response):
            # Log the content of the response
            net = NetworkAnalyser()
            net.record_response()
            # print(f"Outgoing Response Content: {response}")
            # Send the response to the client
            await send(response)

        res = await self.inner(scope, receive_wrapper, send_wrapper)

        return res


# https://book.pythontips.com/en/latest/ternary_operators.html
application = ProtocolTypeRouter(
    {
        "http": (
            PrintHttpRequestMiddleware(django_asgi_app)
            if settings.network_print else django_asgi_app
        ),
        "https": (
            PrintHttpRequestMiddleware(django_asgi_app)
            if settings.network_print else django_asgi_app
        ),
        "websocket": (
            AuthMiddlewareStack(
                PrintHttpRequestMiddleware(URLRouter(websocket_urlpatterns))
            )
            if settings.network_print else
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
if settings.use_ngrok:
    # TODO make a file with setting etc. which is not full of shit
    """Added by ngrok"""
    # This block handles 'make run-django-uvicorn' and 'make run-django-gunicorn' which uses this asgi.py as the entry point.
    # Set env variable to protect against the gunicorn autoreloader.
    if os.getenv("NGROK_LISTENER_RUNNING") is None:
        os.environ["NGROK_LISTENER_RUNNING"] = "true"
        import asyncio, ngrok


        async def setup():
            token = settings.token_ngrok
            subdomain = settings.subdomain_ngrok
            ngrok.set_auth_token(token)
            listen = "localhost:8000"
            listener = await ngrok.forward(addr=listen, domain=subdomain, authtoken=token)
            print(f"Forwarding to {listen} from ingress url: {listener.url()}")
            listener.forward(listen)


        try:
            running_loop = asyncio.get_running_loop()
            running_loop.create_task(setup())
        except RuntimeError:
            # no running loop, run on its own
            asyncio.run(setup())
    """End added by ngrok"""
