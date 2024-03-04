from abc import abstractmethod, ABC
from upstox_client.api_client import ApiClient


class Feeder(ABC):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.connection_thread = None

    @abstractmethod
    def connect(self):
        """Establishes a connection to the data source."""
        pass

    def disconnect(self):
        self.ws.close(status=1000)
