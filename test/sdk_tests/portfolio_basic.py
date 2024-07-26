import upstox_client
import local_storage


def on_message(message):
    print(message)


def on_open():
    print("connection opened")


def main():
    configuration = upstox_client.Configuration()
    configuration.access_token = local_storage.access_token

    streamer = upstox_client.PortfolioDataStreamer(
        upstox_client.ApiClient(configuration))

    streamer.on("message", on_message)
    streamer.on("open", on_open)
    streamer.connect()


if __name__ == "__main__":
    main()
