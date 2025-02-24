from flask import Flask, request, jsonify

from metacognitive.stream.stream_provider.base_stream import BaseStream
import threading

from engine.flow.executor.task_manager import TaskManager

task_manager = TaskManager()

class HTTPStream(BaseStream):
    def __init__(self, port: int = 7072):
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()
        self.start_server()
        self.logs = []

    def setup_routes(self):
        @self.app.route("/get_total_task_count", methods=["GET"])
        def get_total_task_count():
            print("Received total task count request")
            return jsonify({"status": "success", "total_task_count": 10}), 200

        @self.app.route("/get_average_task_duration", methods=["GET"])
        def get_average_task_duration():
            print("Received average task duration request")
            return jsonify({"status": "success", "average_task_duration": 10}), 200
        
        @self.app.route("/get_task_logs", methods=["GET"])
        def get_task_logs():
            res = jsonify({"status": "success", "logs": self.logs}), 200
            self.logs = []
            return res
        
        @self.app.route("/get_task_data", methods=["GET"])
        def get_task_data():
            current_task = task_manager.get_current_task()
            res = jsonify({"status": "success", "current_task": current_task}), 200
            return res
        
        @self.app.route("/levia/chat", methods=["POST"])
        def chat():
            from engine.intent_engine.intent_event import event_chat
            data = request.get_json()
            user_id = data.get('user_id')
            intent = data.get('intent')
            
            if not user_id or not intent:
                return jsonify({"status": "error", "message": "Missing required parameters"}), 400
            
            reply = event_chat(user_id, intent)
            return jsonify({
                "status": "success",
                "reply": reply
            }), 200


    def start_server(self):
        def run_server():
            self.app.run(host="127.0.0.1", port=self.port)

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def output(self, log: str):
        try:
            self.logs.append(log)
        except Exception as e:
            print(f"HTTPStream log error: {e}")
