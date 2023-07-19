from __future__ import print_function
import upstox_client
import ssl
import websockets
import asyncio
import json


def get_portfolio_stream_feed_authorize(api_version, configuration):
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_portfolio_stream_feed_authorize(
        api_version)
    return api_response


async def fetch_order_updates():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Configure OAuth2 access token for authorization: OAUTH2
    configuration = upstox_client.Configuration()

    api_version = '2.0'
    configuration.access_token = 'ACCESS_TOKEN'

    # Get portfolio stream feed authorize
    response = get_portfolio_stream_feed_authorize(
        api_version, configuration)

    async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
        print('Connection established')

        # Perform WebSocket operations
        while True:
            message = await websocket.recv()
            print(json.dumps(message))

asyncio.run(fetch_order_updates())
