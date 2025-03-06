import websocket
import threading
import ssl
from .feeder import Feeder


class PortfolioDataFeeder(Feeder):

    def __init__(self, api_client=None, on_open=None, on_message=None, on_error=None, on_close=None, order_update=True,
                 position_update=False, holding_update=False, gtt_update=False):
        super().__init__(api_client=api_client)
        self.api_client = api_client
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.ws = None
        self.closingCode = -1
        self.order_update = order_update
        self.position_update = position_update
        self.holding_update = holding_update
        self.gtt_update = gtt_update

    def connect(self):
        if self.ws and self.ws.sock:
            return

        sslopt = {
            "cert_reqs": ssl.CERT_NONE,
            "check_hostname": False,
        }
        ws_url = self.get_websocket_url()

        headers = {'Authorization': self.api_client.configuration.auth_settings().get("OAUTH2")[
            "value"]}
        self.ws = websocket.WebSocketApp(ws_url,
                                         header=headers,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        threading.Thread(target=self.ws.run_forever,
                         kwargs={"sslopt": sslopt}).start()

    def get_websocket_url(self):
        ws_url = "wss://api.upstox.com/v2/feed/portfolio-stream-feed"
        update_types = []
        if self.order_update:
            update_types.append("order")
        if self.holding_update:
            update_types.append("holding")
        if self.position_update:
            update_types.append("position")
        if self.gtt_update:
            update_types.append("gtt_order")

        if update_types:
            ws_url += "?update_types=" + "%2C".join(update_types)

        return ws_url
