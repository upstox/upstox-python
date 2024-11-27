import time

import upstox_client
import data_token

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
streamer = upstox_client.MarketDataStreamerV3(
    upstox_client.ApiClient(configuration), instrumentKeys=["NSE_FO|53023", "MCX_FO|428750"], mode="full_d3")

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
time.sleep(10)
print("changing mode to full_d3")
streamer.change_mode(["MCX_FO|428750"], "full_d3")
time.sleep(10)
print("changing mode to ltpc")
streamer.change_mode(["MCX_FO|428750"], "ltpc")

