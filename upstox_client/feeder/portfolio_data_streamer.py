from .portfolio_data_feeder import PortfolioDataFeeder
from .streamer import Streamer


class PortfolioDataStreamer(Streamer):

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.api_client = api_client
        self.feeder = None

    def connect(self):
        self.feeder = PortfolioDataFeeder(
            api_client=self.api_client, on_open=self.handle_open, on_message=self.handle_message, on_error=self.handle_error, on_close=self.handle_close)
        self.feeder.connect()

    def handle_open(self, ws):
        self.disconnect_valid = False
        self.reconnect_in_progress = False
        self.reconnect_attempts = 0
        self.emit(self.Event["OPEN"])

    def handle_message(self, ws, message):
        self.emit(self.Event["MESSAGE"], message)

