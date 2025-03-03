# Import stream providers
from metacognitive.stream.stream_provider.base_stream import BaseStream
from metacognitive.stream.stream_provider.log_stream.log_stream import LogStream
from metacognitive.stream.stream_provider.http_stream.http_stream import HTTPStream
from metacognitive.stream.stream_provider.local_stream.local_stream import LocalStream
from metacognitive.stream.stream_provider.log_stream.remote_log_stream import RemoteLogStream
from metacognitive.stream.stream_provider.websocket_stream.websocket_stream import (
    WebsocketStream,
)


class Stream:
    """
    Stream class that manages multiple output streams.
    Supports HTTP, local file, and WebSocket output streams.
    """

    def __init__(self, stream_types=["local"]):
        """
        Initialize Stream with specified stream type.

        Args:
            stream_type (str): Type of stream to initialize ("http", "local", or "websocket")
        """
        self.streams = []
        for stream_type in stream_types:
            if stream_type == "http":
                self.add_stream(HTTPStream(7072))
            elif stream_type == "local":
                self.add_stream(LocalStream())
            elif stream_type == "websocket":
                self.add_stream(WebsocketStream("ws://localhost:8765"))
            elif stream_type == "remote_log":
                self.add_stream(RemoteLogStream())
            else:
                raise ValueError(f"Invalid stream type: {stream_type}")

        # Always add log stream as secondary output
        self.add_stream(LogStream())

    def add_stream(self, stream: BaseStream):
        """
        Add a new output stream.

        Args:
            stream (BaseStream): Stream instance to add
        """
        self.streams.append(stream)

    def output(self, log: str, user_id: str, type: str, ch_id: str):
        """
        Output log message to all registered streams.

        Args:
            log (str): Message to output
        """
        for stream in self.streams:
            stream.output(log, user_id, type, ch_id)


# Global singleton instance
_stream = None


def output_stream(log: str, user_id: str = "levia", type: str = "info", ch_id: str = ""):
    """
    Global function to output to stream singleton.
    Creates WebSocket stream instance if none exists.

    Args:
        log (str): Message to output
        user_id (str): User identifier
        type (str): Message type
        ch_id (str): channel identifier (current dialog id
    """
    global _stream
    if _stream is None:
        _stream = Stream(stream_types=["remote_log", "local", "http"])
    _stream.output(log, user_id, type, ch_id)
