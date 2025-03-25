from flask import Flask, request, jsonify, Response
from metacognitive.stream.stream_provider.base_stream import BaseStream
import threading
import json
import redis
import time
import uuid
from memory.db_connection.redis_connector import RedisUtils
from metacognitive.stream.stream_provider.http_stream.api_key_manager import require_api_key, api_key_manager
redis_tool = RedisUtils()

class HTTPStream(BaseStream):
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, port: int = 7072):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, port: int = 7072):
        if self._initialized:
            return
            
        self.port = port
        self.app = Flask(__name__)
        
        self.pubsub = redis_tool.pubsub()
        
        self.setup_routes()
        self.start_server()
        self.logs = []
        
        # Generate unique node ID to identify the current server instance
        self.node_id = str(uuid.uuid4())
        print(f"Node {self.node_id} started")
        
        self._initialized = True

    def setup_routes(self):

        @self.app.route("/levia/chat/create", methods=["POST"])
        @require_api_key
        def create_chat_session():
            try:
                data = request.get_json()
                user_id = data.get('user_id')
                
                if not user_id:
                    return jsonify({
                        "status": "error",
                        "message": "Missing user_id parameter"
                    }), 400
                
                session_id = str(uuid.uuid4())
                
                # Store session info with its own TTL
                session_info_key = f"chat:session:{session_id}"
                redis_tool.setex(key=session_info_key, value=user_id, time=259200)
                
                # Add to user's session set without updating its TTL
                user_sessions_key = f"chat:sessions:{user_id}"
                if not redis_tool.exists(user_sessions_key):
                    redis_tool.set_add(user_sessions_key, session_id)
                    redis_tool.expire(user_sessions_key, 259200)
                else:
                    redis_tool.set_add(user_sessions_key, session_id)
                
                return jsonify({
                    "status": "success",
                    "session_id": session_id,
                    "message": "New chat session created"
                }), 201
                
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 500
        
        @self.app.route("/levia/chat", methods=["POST"])
        @require_api_key
        def chat():
            from engine.intent_engine.intent_event import event_chat
            data = request.get_json()
            user_id = data.get('user_id')
            intent = data.get('intent')
            session_id = data.get('session_id')
            
            session_key = f"chat:session:{session_id}"
            user_sessions_key = f"chat:sessions:{user_id}"
            
            if not redis_tool.exists(session_key):
                return jsonify({
                    "status": "error",
                    "message": "Session ID does not exist or has expired"
                }), 401
            
            if not redis_tool.ismember(user_sessions_key, session_id):
                return jsonify({
                    "status": "error",
                    "message": "Session ID does not belong to this user"
                }), 401
            
            # Generate unique request ID
            request_id = str(uuid.uuid4())
            
            # Create request processing status key to track which node is processing the request
            processing_key = f"chat:processing:{request_id}"
            # Set processing status with 1 hour TTL to prevent permanent state in case of task abnormality
            redis_tool.setex(key=processing_key, value=self.node_id, time=1800)
            
            # Save user ID and request ID mapping in Redis for client connection
            user_request_key = f"user:request:{user_id}"
            redis_tool.setex(key=user_request_key, value=request_id, time=1800)
            
            # Process chat request in a new thread
            def process_chat():
                try:
                    reply = event_chat(user_id, intent, session_id)
                    
                    # Publish completion message after processing
                    complete_message = json.dumps({
                        "type": "complete",
                        "data": {"reply": reply}
                    })
                    redis_tool.publish(channel=f"chat:events:{request_id}", message=complete_message)
                    
                    # Clean up Redis keys after successful completion
                    self._cleanup_request_data(request_id, user_id)
                    
                    # Set result cache for reconnection with shorter TTL
                    result_key = f"chat:result:{request_id}"
                    redis_tool.setex(key=result_key, value=complete_message, time=300)  # 5 minutes cache
                except Exception as e:
                    # Send error message
                    error_message = json.dumps({
                        "type": "error",
                        "data": {"error": str(e)}
                    })
                    redis_tool.publish(channel=f"chat:events:{request_id}", message=error_message)
                    # Clean up on error as well
                    self._cleanup_request_data(request_id, user_id)
            
            # Start processing thread
            threading.Thread(target=process_chat).start()
            
            # Return request ID to client for connecting to SSE stream
            return jsonify({
                "status": "success",
                "request_id": request_id,
                "message": f"Processing started, connect to /levia/chat/stream/{request_id} for updates"
            }), 202
        
        @self.app.route("/levia/chat/stream/<request_id>", methods=["GET"])
        @require_api_key
        def chat_stream(request_id):
            def generate():
                # Check if there's a cached result
                result_key = f"chat:result:{request_id}"

                cached_result = redis_tool.get_json_value(key=result_key)
                if cached_result:
                    cached_result = cached_result if isinstance(cached_result, str) else cached_result.decode('utf-8')
                    yield f"data: {cached_result}\n\n"
                    return
                
                # Subscribe to the event channel for this request
                channel = f"chat:events:{request_id}"
                pubsub = redis_tool.pubsub()
                pubsub.subscribe(channel)
                
                try:
                    # Get existing logs for log recovery during reconnection
                    logs_key = f"chat:logs:{request_id}"
                    existing_logs = redis_tool.list_range(logs_key, 0, -1)
                    for log in existing_logs:
                        log_str = log if isinstance(log, str) else log.decode('utf-8')
                        yield f"data: {log_str}\n\n"
                        try:
                            log_data = json.loads(log_str)
                            if log_data.get('type') in ['complete', 'error']:
                                return
                        except:
                            pass
                    
                    # Check if the request is still being processed
                    processing_key = f"chat:processing:{request_id}"
                    if not redis_tool.exists(processing_key):
                        # If the request is not being processed and there's no cached result, it might be an invalid request ID
                        error_message = json.dumps({
                            "type": "error",
                            "data": {"error": "Invalid or expired request ID"}
                        })
                        yield f"data: {error_message}\n\n"
                        return
                    
                    # Listen for real-time messages
                    while True:
                        message = pubsub.get_message()
                        if message:
                            data = message['data']
                            yield f"data: {data}\n\n"
                            
                            # Check if it's a completion or error message
                            try:
                                msg_data = json.loads(data)
                                if msg_data.get('type') in ['complete', 'error']:
                                    break
                            except:
                                pass
                        
                        # Check if the request is still being processed
                        if not redis_tool.exists(processing_key):
                            break
                            
                        time.sleep(1)
                finally:
                    pubsub.unsubscribe()
            
            # Return SSE stream response
            return Response(generate(), mimetype="text/event-stream", 
                           headers={
                               "Cache-Control": "no-cache",
                               "X-Accel-Buffering": "no",
                               "Connection": "keep-alive"
                           })
        
        # New endpoint: Get current request ID by user ID
        @self.app.route("/levia/chat/request/<user_id>", methods=["GET"])
        @require_api_key
        def get_user_request(user_id):
            user_request_key = f"user:request:{user_id}"
            request_id = redis_tool.get_value(user_request_key)
            
            if request_id:
                return jsonify({
                    "status": "success",
                    "request_id": request_id if isinstance(request_id, str) else request_id.decode('utf-8')
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "No active request found for this user"
                }), 404

    def start_server(self):
        import os
        if os.environ.get('INTERACTION_MODE') != 'server':
            def run_server():
                self.app.run(host="0.0.0.0", port=self.port, threaded=True)
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()

    def output(self, log: str, user_id: str, type: str, ch_id: str = "", title: str = "", api_key: str = "", dev_id: str = ""):
        if type == "end_time" or "Final reply" in log or "Final reply" in title:
            return
        try:
            self.logs.append(log)
            
            # Find the request ID associated with the user
            user_request_key = f"user:request:{user_id}"
            request_id = redis_tool.get_value(user_request_key)
            
            if request_id:
                request_id = request_id if isinstance(request_id, str) else request_id.decode('utf-8')
                
                # Create log message
                message = json.dumps({
                    "type": "stream",
                    "data": {
                        "content": log,
                        "type": type,
                        "ch_id": ch_id
                    }
                })
                
                # Save log to Redis list for history during reconnection
                logs_key = f"chat:logs:{request_id}"
                redis_tool.list_push(logs_key, message)
                redis_tool.expire(logs_key, 1800)  # Set 1 hour expiration time
                
                # Publish log to event stream
                redis_tool.publish(f"chat:events:{request_id}", message)
        except Exception as e:
            print(f"HTTPStream log error: {e}")

    def _cleanup_request_data(self, request_id: str, user_id: str):
        """Clean up Redis keys associated with a request"""
        keys_to_delete = [
            f"chat:processing:{request_id}",
            f"user:request:{user_id}",
            f"chat:logs:{request_id}"
        ]
        for key in keys_to_delete:
            redis_tool.delete(key)