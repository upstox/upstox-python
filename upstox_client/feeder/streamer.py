from abc import abstractmethod, ABC
import time


class Streamer(ABC):
    Event = {
        "OPEN": "open",
        "CLOSE": "close",
        "MESSAGE": "message",
        "ERROR": "error",
        "RECONNECTING": "reconnecting",
        "AUTO_RECONNECT_STOPPED": "autoReconnectStopped"
    }

    def __init__(self, api_client=None):
        self.feeder = None
        self.listeners = {event_name: [] for event_name in self.Event.values()}
        self.disconnect_valid = False
        self.reconnect_in_progress = False
        self.enable_auto_reconnect = True
        self.interval = 1  # Interval between reconnection attempts
        self.retry_count = 5  # Maximum number of reconnection attempts
        self.reconnect_attempts = 0  # Current count of reconnection attempts

    def on(self, event, listener):
        """Registers a new listener for an event."""
        if event in self.listeners:
            self.listeners[event].append(listener)
        else:
            raise ValueError(f"Unknown event: {event}")

    def emit(self, event, *args):
        """Emits an event to all registered listeners."""
        if event in self.listeners:
            for listener in self.listeners[event]:
                # Call the listener. If it's a regular function, it's called directly.
                # If it's meant to be run in a separate thread, it's the caller's responsibility to ensure that.
                listener(*args)
        else:
            raise ValueError(f"Unknown event: {event}")

    @abstractmethod
    def connect(self):
        """Initates a connection with the appropriate Feeder."""
        pass

    def disconnect(self):
        """Initiates the disconnection process."""
        if self.feeder:
            self.disconnect_valid = True
            self.feeder.disconnect()
        else:
            raise NotImplementedError("Feeder instance not set.")

    def auto_reconnect(self, enable, interval=1, retry_count=5):
        self.enable_auto_reconnect = enable
        self.interval = interval
        self.retry_count = retry_count
        if not enable:
            self.emit(self.Event["AUTO_RECONNECT_STOPPED"],
                      "Disabled by client.")

    def launch_auto_reconnect(self):
        """Starts the auto-reconnect process."""
        if self.enable_auto_reconnect:
            self.reconnect_in_progress = True
            self.reconnect_attempts += 1
            self.emit(self.Event["RECONNECTING"],
                      f"Auto reconnect attempt {self.reconnect_attempts}/{self.retry_count}")
            self.connect()  # Initial reconnect attempt

    @abstractmethod
    def handle_open(self, ws):
        """Defines the logic to prepare socket for usage on open."""
        pass

    @abstractmethod
    def handle_message(self, ws, message):
        """Defines the logic to handle incoming messages over the socket."""
        pass

    def handle_error(self, ws, error):
        self.emit(self.Event["ERROR"], error)

        if "401 Unauthorized" in str(error):
            # Do not re-attempt connection on 401
            self.disconnect_valid = True
            return

        if self.enable_auto_reconnect and self.reconnect_in_progress and self.reconnect_attempts < self.retry_count:
            # Increment reconnect attempts and possibly trigger another reconnect
            time.sleep(self.interval)
            self.reconnect_attempts += 1
            self.emit(self.Event["RECONNECTING"],
                      f"Auto reconnect attempt {self.reconnect_attempts}/{self.retry_count}")
            self.connect()  # Attempt to reconnect
            return

        if self.reconnect_attempts == self.retry_count:
            self.emit(self.Event["AUTO_RECONNECT_STOPPED"],
                      f"retryCount of {self.retry_count} exhausted.")

    def handle_close(self, ws, close_status_code, close_msg):
        if not self.reconnect_in_progress:
            self.emit(self.Event["CLOSE"], close_status_code, close_msg)

        if not self.reconnect_in_progress and not self.disconnect_valid and close_status_code != 1000:
            self.launch_auto_reconnect()
            return
