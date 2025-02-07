from metacognitive.stream.stream_provider.base_stream import BaseStream


class LocalStream(BaseStream):
    def __init__(self):
        pass

    def output(self, log: str):
        try:
            print(log)
        except Exception as e:
            print(f"LocalStream write log error: {e}")
