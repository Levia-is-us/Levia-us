from metacognitive.stream.stream_provider.base_stream import BaseStream


class LocalStream(BaseStream):
    def __init__(self):
        pass

    def output(self, log: str, user_id: str, type: str):
        try:
            print(f"\033[95m{log}\033[0m")
        except Exception as e:
            print(f"LocalStream write log error: {e}")
