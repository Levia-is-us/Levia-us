import os
from datetime import datetime
from metacognitive.stream.stream_provider.base_stream import BaseStream


class LogStream(BaseStream):
    def __init__(self):
        self.logs_dir = os.path.join("metacognitive", "stream", "logs")
        os.makedirs(self.logs_dir, exist_ok=True)

    def output(self, log: str, user_id: str, type: str):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            date_hour = current_time.strftime("%Y-%m-%d_%H")
            filename = os.path.join(self.logs_dir, f"{date_hour}.log")
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {log}\n")
        except Exception as e:
            print(f"LocalStream write log error: {e}")
