from flask import request, jsonify
import threading
import time
from datetime import datetime, timedelta
from memory.db_connection.mysql_connector import MySQLPool

db_pool = MySQLPool()

class APIKeyManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.api_keys = {}  # {api_key: expiry_time}
        
        # Start the cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_expired_keys, daemon=True)
        self.cleanup_thread.start()
        
        self._initialized = True
    
    def validate_key(self, api_key):
        """Validate if API key is valid and not expired"""
        now = datetime.now()
        
        # Check if key exists in memory cache and is not expired
        if api_key in self.api_keys and self.api_keys[api_key] > now:
            return True
            
        # If key not in cache or expired, check database
        try:
            sql = """select api_key from levia_api_keys where api_key = %s and `status` = 'active'"""
            result = db_pool.query_one(sql, (api_key))
            
            if result:
                # Update memory cache with 30 min expiry
                self.api_keys[api_key] = now + timedelta(minutes=30)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Database query error: {e}")
            return False
    
    def _cleanup_expired_keys(self):
        """Periodically clean up expired keys from memory"""
        while True:
            time.sleep(60)  # Check every minute
            now = datetime.now()
            expired_keys = [k for k, exp in self.api_keys.items() if exp <= now]
            
            for key in expired_keys:
                del self.api_keys[key]

# Create singleton instance
api_key_manager = APIKeyManager()

def require_api_key(f):
    """Decorator to require valid API key for routes"""
    def decorated(*args, **kwargs):
        api_key = None
        
        # Try to get API key from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            api_key = auth_header[7:]  # Remove 'Bearer ' prefix
        
        # Also check for API key in query parameters
        if not api_key:
            api_key = request.args.get('api_key')
            
        # Validate API key
        if api_key and api_key_manager.validate_key(api_key):
            from metacognitive.stream.stream import output_stream
            output_stream(f"API key : {api_key} request: {request.path}", api_key, "info", "", "Authorization")
            return f(*args, **kwargs)
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid or missing API key"
            }), 401
            
    # Preserve the original function's attributes
    decorated.__name__ = f.__name__
    return decorated