import upstox_client
import data_token


def on_message(message):
    print(message)


def on_open():
    print("connection opened")


def main():
    configuration = upstox_client.Configuration()
    configuration.access_token = data_token.access_token

    streamer = upstox_client.PortfolioDataStreamer(
        upstox_client.ApiClient(configuration))

    streamer.on("message", on_message)
    streamer.on("open", on_open)
    streamer.connect()


if __name__ == "__main__":
    main()
