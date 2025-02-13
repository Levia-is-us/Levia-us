from flask import Flask, request, jsonify

from metacognitive.stream.stream_provider.base_stream import BaseStream
import threading


class HTTPStream(BaseStream):
    def __init__(self, port: int = 7072):
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()
        self.start_server()

    def setup_routes(self):
        @self.app.route("/get_total_task_count", methods=["GET"])
        def get_total_task_count():
            print("Received total task count request")
            return jsonify({"status": "success", "total_task_count": 10}), 200

        @self.app.route("/get_average_task_duration", methods=["GET"])
        def get_average_task_duration():
            print("Received average task duration request")
            return jsonify({"status": "success", "average_task_duration": 10}), 200

    def start_server(self):
        def run_server():
            self.app.run(host="127.0.0.1", port=self.port)

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def output(self, log: str):
        try:
            # print(f"Log received by server: {log}")
            pass
        except Exception as e:
            print(f"HTTPStream log error: {e}")
