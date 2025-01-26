import upstox_client
import data_token

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
streamer = upstox_client.MarketDataStreamer(
    upstox_client.ApiClient(configuration), instrumentKeys=["MCX_FO|442169"], mode="full")

streamer.auto_reconnect(True, 5, 10)


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
