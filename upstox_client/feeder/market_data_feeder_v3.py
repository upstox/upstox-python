import websocket
import json
import uuid
import threading
import ssl
from .feeder import Feeder


class MarketDataFeederV3(Feeder):
    Mode = {
        "LTPC": "ltpc",
        "FULL": "full",
        "OPTION": "option_greeks",
        "D30": "full_d30"
    }

    Method = {
        "SUBSCRIBE": "sub",
        "CHANGE_METHOD": "change_mode",
        "UNSUBSCRIBE": "unsub",
    }

    def __init__(self, api_client=None, instrumentKeys=[], mode="full", on_open=None, on_message=None, on_error=None, on_close=None):
        super().__init__(api_client=api_client)
        self.api_client = api_client
        self.instrumentKeys = instrumentKeys
        self.mode = mode
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.ws = None
        self.closingCode = -1

    def connect(self):
        if self.ws and self.ws.sock:
            return

        sslopt = {
            "cert_reqs": ssl.CERT_NONE,
            "check_hostname": False,
        }
        ws_url = "wss://api.upstox.com/v3/feed/market-data-feed"
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

    def subscribe(self, instrumentKeys, mode=None):
        if self.ws and self.ws.sock:
            request = self.build_request(
                instrumentKeys, self.Method["SUBSCRIBE"], mode)
            self.ws.send(request, opcode=websocket.ABNF.OPCODE_BINARY)
        else:
            raise Exception("WebSocket is not open.")

    def unsubscribe(self, instrumentKeys):
        if self.ws and self.ws.sock:
            request = self.build_request(
                instrumentKeys, self.Method["UNSUBSCRIBE"])
            self.ws.send(request, opcode=websocket.ABNF.OPCODE_BINARY)
        else:
            raise Exception("WebSocket is not open.")

    def change_mode(self, instrumentKeys, newMode):

        if self.ws and self.ws.sock:
            request = self.build_request(
                instrumentKeys, self.Method["CHANGE_METHOD"], newMode)
            self.ws.send(request, opcode=websocket.ABNF.OPCODE_BINARY)
        else:
            raise Exception("WebSocket is not open.")

    def build_request(self, instrumentKeys, method, mode=None):
        requestObj = {
            "guid": str(uuid.uuid4()),
            "method": method,
            "data": {
                "instrumentKeys": instrumentKeys,
            },
        }
        if mode is not None:
            requestObj["data"]["mode"] = mode

        return json.dumps(requestObj).encode('utf-8')
