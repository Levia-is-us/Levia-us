# Import stream providers
from metacognative.stream.stream_provider.base_stream import BaseStream
from metacognative.stream.stream_provider.log_stream.log_stream import LogStream
from metacognative.stream.stream_provider.http_stream.http_stream import HTTPStream
from metacognative.stream.stream_provider.local_stream.local_stream import LocalStream
from metacognative.stream.stream_provider.websocket_stream.websocket_stream import (
    WebsocketStream,
)


class Stream:
    """
    Stream class that manages multiple output streams.
    Supports HTTP, local file, and WebSocket output streams.
    """

    def __init__(self, stream_type="local"):
        """
        Initialize Stream with specified stream type.
        
        Args:
            stream_type (str): Type of stream to initialize ("http", "local", or "websocket")
        """
        self.streams = []
        if stream_type == "http":
            self.add_stream(HTTPStream("http://localhost:8000/log"))
        elif stream_type == "local":
            self.add_stream(LocalStream())
        elif stream_type == "websocket":
            self.add_stream(WebsocketStream("ws://localhost:8765/log"))
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

    def output(self, log: str):
        """
        Output log message to all registered streams.
        
        Args:
            log (str): Message to output
        """
        for stream in self.streams:
            stream.output(log)


# Global singleton instance
_stream = None


def output_stream(log: str):
    """
    Global function to output to stream singleton.
    Creates WebSocket stream instance if none exists.
    
    Args:
        log (str): Message to output
    """
    global _stream
    if _stream is None:
        _stream = Stream(stream_type="websocket")
    _stream.output(log)
