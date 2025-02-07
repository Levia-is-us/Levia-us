import requests
from metacognitive.stream.stream_provider.base_stream import BaseStream


class HTTPStream(BaseStream):
    def __init__(self, url: str):
        self.url = url

    def output(self, log: str):
        try:
            response = requests.post(self.url, json={"log": log})
            response.raise_for_status()
        except Exception as e:  
            print(f"HTTPStream send log error: {e}")
