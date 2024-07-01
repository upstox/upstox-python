import upstox_client
import websocket

configuration = upstox_client.Configuration()

access_token = "access_token"

configuration.access_token = access_token
streamer = upstox_client.PortfolioDataStreamer(upstox_client.ApiClient(configuration),order_update=False,holding_update=True,position_update=False)

def on_open():
    print("on open message")


def close(a, b):
    print(f"on close message {a}")


def message(data):
    print(f"on message message{data}")


def error(er):
    print(f"on error message= {er}")


def reconnecting(data):
    print(f"reconnecting event= {data}")


streamer.on("open", on_open)
streamer.on("message", message)
streamer.on("close", close)
streamer.on("reconnecting", reconnecting)
streamer.on("error", error)
streamer.connect()
