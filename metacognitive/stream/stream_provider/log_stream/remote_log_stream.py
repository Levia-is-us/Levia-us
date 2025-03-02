import os
from metacognitive.stream.stream_provider.base_stream import BaseStream
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
from typing import Dict
from concurrent.futures import ThreadPoolExecutor
import time

ENVIRONMENT=os.getenv("ENVIRONMENT", "local")
LOG_URL=os.getenv("LEVIA_LOG_SERVER", "")
VISUAL = os.getenv("VISUAL", False)

class RemoteLogStream(BaseStream):
    def __init__(self):
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[404, 500, 502, 503, 504],
            allowed_methods=["POST"],
            raise_on_status=True
        )
        
        # Configure adapter
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=60,
            max_retries=retry_strategy,
            pool_block=False
        )
        
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.session.headers.update({
            'Connection': 'keep-alive',
            'Keep-Alive': 'timeout=60, max=1000'
        })

        # Dictionary to store locks for each chid
        self.locks: Dict[str, threading.Lock] = {}
        self.locks_lock = threading.Lock()
        
        # Add thread pool to limit concurrent threads
        self.executor = ThreadPoolExecutor(max_workers=20)
        
        # Add lock expiration cleanup
        self.last_used: Dict[str, float] = {}
        self.cleanup_thread = threading.Thread(target=self._cleanup_locks, daemon=True)
        self.cleanup_thread.start()

    def __del__(self):
        # Ensure session and thread pool are closed when object is destroyed
        self.session.close()
        self.executor.shutdown(wait=False)

    def get_lock_for_chid(self, ch_id: str) -> threading.Lock:
        with self.locks_lock:
            if ch_id not in self.locks:
                self.locks[ch_id] = threading.Lock()
            # Update last used time
            self.last_used[ch_id] = time.time()
            return self.locks[ch_id]
    
    def _cleanup_locks(self):
        """Periodically clean up locks that haven't been used for a while"""
        while True:
            time.sleep(300)  # Clean up every 5 minutes
            current_time = time.time()
            with self.locks_lock:
                to_remove = []
                for ch_id, last_time in self.last_used.items():
                    if current_time - last_time > 60:  # Remove if unused for 60s
                        to_remove.append(ch_id)
                
                for ch_id in to_remove:
                    del self.locks[ch_id]
                    del self.last_used[ch_id]
                    
                print(f"Cleaned up {len(to_remove)} unused locks. Current locks: {len(self.locks)}")

    def output(self, log: str, user_id: str, type: str, ch_id: str):
        try:
            if ENVIRONMENT == "local" or (not log or not log.strip() or "Initialized metacognitive stream." in log):
                return

            # Replace - with /n
            log = log.replace(" - ", "\n")
            # Remove extra \n and spaces
            log = log.strip()
            # Replace multiple consecutive newlines with a single newline
            while "\n\n" in log or "  " in log:
                log = log.replace("\n\n", "\n")
                log = log.replace("  ", " ")
            log = log.strip()
            
            if log == "":
                return
            
            payload = {
                "user_id": user_id,
                "intent": log,
                "type": type,
                "visual": VISUAL,
                "chid": ch_id
            }
            
            # Submit task to thread pool instead of creating new thread
            self.executor.submit(self._send_log, payload, ch_id)
        except Exception as e:
            print(f"Error sending log: {str(e)}")
        
    def _send_log(self, payload, ch_id):
        # Get or create lock for this chid
        lock = self.get_lock_for_chid(ch_id)
        
        # Ensure sequential processing for the same chid
        with lock:
            try:
                # Add timeout settings
                response = self.session.post(LOG_URL, json=payload, timeout=(3.05, 27))
                response.raise_for_status()
                return response.text
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {str(e)}")
                return None
            except requests.exceptions.Timeout as e:
                print(f"Request timeout: {str(e)}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"Request error: {str(e)}")
                return None