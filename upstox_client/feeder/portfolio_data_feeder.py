import websocket
from .feeder import Feeder
import ssl


class PortfolioDataFeeder(Feeder):

    def __init__(self, api_client=None, on_open=None, on_message=None, on_error=None, on_close=None):
        super().__init__(api_client=api_client)
        self.api_client = api_client
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.ws = None
        self.closingCode = -1

    def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        sslopt = {
            "cert_reqs": ssl_context.verify_mode,
            "check_hostname": ssl_context.check_hostname,
        }
        if self.ws and self.ws.sock:
            return

        ws_url = "wss://api.upstox.com/v2/feed/portfolio-stream-feed"
        headers = {'Authorization': self.api_client.configuration.auth_settings().get("OAUTH2")[
            "value"]}
        self.ws = websocket.WebSocketApp(ws_url,
                                         header=headers,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever(sslopt=sslopt)
