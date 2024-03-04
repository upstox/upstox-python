from .market_data_feeder import MarketDataFeeder
from .streamer import Streamer
from .proto import MarketDataFeed_pb2
from google.protobuf import json_format


class MarketDataStreamer(Streamer):
    Mode = {
        "LTPC": "ltpc",
        "FULL": "full",
    }

    def __init__(self, api_client=None, instrumentKeys=[], mode=""):
        super().__init__(api_client)
        self.protobufRoot = MarketDataFeed_pb2
        self.api_client = api_client
        self.instrumentKeys = instrumentKeys
        self.mode = mode
        self.subscriptions = {
            self.Mode["LTPC"]: set(),
            self.Mode["FULL"]: set(),
        }
        # Populate initial subscriptions if provided
        for key in instrumentKeys:
            self.subscriptions[mode].add(key)

    def connect(self):
        self.feeder = MarketDataFeeder(
            api_client=self.api_client, instrumentKeys=self.instrumentKeys, mode=self.mode, on_open=self.handle_open, on_message=self.handle_message, on_error=self.handle_error, on_close=self.handle_close)
        self.feeder.connect()

    def subscribe_to_initial_keys(self):
        for mode, keys in self.subscriptions.items():
            if keys:
                self.feeder.subscribe(list(keys), mode)

    def subscribe(self, instrumentKeys, mode):
        if not self.feeder:
            raise Exception("WebSocket is not open.")

        self.feeder.subscribe(instrumentKeys, mode)
        self.subscriptions[mode].update(instrumentKeys)

    def unsubscribe(self, instrumentKeys):
        self.feeder.unsubscribe(instrumentKeys)
        for mode_keys in self.subscriptions.values():
            mode_keys.difference_update(instrumentKeys)

    def change_mode(self, instrumentKeys, newMode):
        if not self.feeder:
            raise Exception("WebSocket is not open.")

        oldMode = self.Mode["LTPC"] if newMode == self.Mode["FULL"] else self.Mode["FULL"]
        self.feeder.change_mode(instrumentKeys, newMode)
        # Remove keys from the old mode
        self.subscriptions[oldMode].difference_update(instrumentKeys)
        # Add keys to the new mode
        self.subscriptions[newMode].update(instrumentKeys)

    def clear_subscriptions(self):
        for mode_keys in self.subscriptions.values():
            mode_keys.clear()

    def decode_protobuf(self, buffer):
        FeedResponse = self.protobufRoot.FeedResponse
        return FeedResponse.FromString(buffer)

    def handle_open(self, ws):
        self.disconnect_valid = False
        self.reconnect_in_progress = False
        self.reconnect_attempts = 0
        self.subscribe_to_initial_keys()
        self.emit(self.Event["OPEN"])

    def handle_message(self, ws, message):
        decoded_data = self.decode_protobuf(message)
        data_dict = json_format.MessageToDict(decoded_data)
        self.emit(self.Event["MESSAGE"], data_dict)
