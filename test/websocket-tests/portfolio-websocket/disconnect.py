
import time
import upstox_client

configuration = upstox_client.Configuration()
access_token = "access_token"
configuration.access_token = access_token
streamer = upstox_client.PortfolioDataStreamer(
    upstox_client.ApiClient(configuration))


streamer.auto_reconnect(True, 5, 10)
def on_open():
    print("on open message")

def close(a, b):
    print(f"on close message {a}")


def message(data):
    print(f"on message message{data}")


def error(er):
    print(f"on error message= {er}")


def disconnection():
    time.sleep(10)
    streamer.disconnect()

def f_disconnection():
    time.sleep(15)
    streamer.disconnect()

def reconnecting(data):
    print(f"reconnecting event= {data}")

streamer.on("open", on_open)
streamer.on("message", message)
streamer.on("close", close)
streamer.on("reconnecting", reconnecting)
streamer.on("error", error)

streamer.connect()
disconnection()
f_disconnection()

