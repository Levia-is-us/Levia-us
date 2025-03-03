import requests
import json
import random
import time
import threading

# Base URL for all API requests
BASE_URL = 'http://127.0.0.1:7072/levia'

def create_chat_session(user_id):
    """
    Create a new chat session for a user
    
    Args:
        user_id (str): The user's ID
        
    Returns:
        str or None: Session ID if successful, None otherwise
    """
    try:
        response = requests.post(
            f"{BASE_URL}/chat/create",
            json={"user_id": user_id},
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        
        if response.status_code == 201:
            return data.get("session_id")
        else:
            print(f"Failed to create chat session: {data.get('message')}")
            return None
    except Exception as e:
        print(f"Error creating chat session: {str(e)}")
        return None

def send_chat_message(user_id, message, session_id):
    """
    Send a chat message
    
    Args:
        user_id (str): The user's ID
        message (str): The message to send
        session_id (str): The session ID
        
    Returns:
        str or None: Request ID if successful, None otherwise
    """
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "user_id": user_id,
                "intent": message,
                "session_id": session_id
            },
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        
        if response.status_code == 202:
            return data.get("request_id")
        else:
            print(f"Failed to send chat message: {data.get('message')}")
            return None
    except Exception as e:
        print(f"Error sending chat message: {str(e)}")
        return None

def connect_to_stream(request_id):
    """
    Connect to the SSE stream to receive responses
    
    Args:
        request_id (str): The request ID to connect to
        
    Returns:
        Thread: The thread handling the SSE connection
    """
    def stream_listener():
        """Background thread function to listen to the SSE stream"""
        try:
            url = f"{BASE_URL}/chat/stream/{request_id}"
            headers = {'Accept': 'text/event-stream'}
            
            response = requests.get(url, headers=headers, stream=True)
            
            print("SSE connection established")
            
            # Manual parsing of SSE events
            buffer = ""
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    buffer += chunk.decode('utf-8')
                    # Process any complete events in the buffer
                    while '\n\n' in buffer:
                        event, buffer = buffer.split('\n\n', 1)
                        # Parse the event data
                        for line in event.split('\n'):
                            if line.startswith('data:'):
                                data_str = line[5:].strip()
                                try:
                                    data = json.loads(data_str)
                                    
                                    if data.get("type") == "stream":
                                        print(f"[stream] {data['data']['content']}")
                                    elif data.get("type") == "complete":
                                        print("\n=== Response Received ===")
                                        print(data["data"]["reply"])
                                        print("=========================")
                                        return  # Exit the thread when complete
                                    elif data.get("type") == "error":
                                        print("\n=== Error Received ===")
                                        print(data["data"]["error"])
                                        print("======================")
                                        return  # Exit the thread on error
                                    else:
                                        print(f"[UNKNOWN] {data_str}")
                                except json.JSONDecodeError as e:
                                    print(f"Error parsing event data: {str(e)}")
        except Exception as e:
            print(f"SSE connection error: {str(e)}")
    
    # Start the streaming in a background thread
    thread = threading.Thread(target=stream_listener)
    thread.daemon = True
    thread.start()
    return thread

def get_active_request(user_id):
    """
    Check if there's an active request for a user
    
    Args:
        user_id (str): The user's ID
        
    Returns:
        str or None: Request ID if active, None otherwise
    """
    try:
        response = requests.get(f"{BASE_URL}/chat/request/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get("request_id")
        elif response.status_code == 404:
            return None
        else:
            print("Error checking active request")
            return None
    except Exception as e:
        print(f"Error checking active request: {str(e)}")
        return None

def main():
    """Main function to demonstrate HTTP Stream API usage"""
    try:
        print("Starting HTTP Stream API client...")
        
        # Configuration
        user_id = f"user_{random.randint(1000, 9999)}"
        user_message = "Tell me about the weather today"
        
        print(f"User ID: {user_id}")
        print(f"Message: \"{user_message}\"")
        
        # Step 1: Create a chat session
        print("\n=== Step 1: Creating chat session ===")
        session_id = create_chat_session(user_id)
        if not session_id:
            raise Exception("Failed to create chat session")
        print(f"Session created successfully with ID: {session_id}")
        
        # Step 2: Send a chat message
        print("\n=== Step 2: Sending chat message ===")
        request_id = send_chat_message(user_id, user_message, session_id)
        if not request_id:
            raise Exception("Failed to send chat message")
        print(f"Message sent successfully with request ID: {request_id}")
        
        # Step 3: Connect to the stream
        print("\n=== Step 3: Connecting to response stream ===")
        stream_thread = connect_to_stream(request_id)
        
        # Wait a bit and then check active request status
        time.sleep(5)
        print("\n=== Step 4: Checking active request status ===")
        active_request_id = get_active_request(user_id)
        if active_request_id:
            print(f"Active request found: {active_request_id}")
        else:
            print("No active request found (processing may be complete)")
        
        # Keep the main thread alive while the stream is processing
        print("\nAll steps completed. The stream will continue to receive messages until completion.")
        
        # 等待stream线程完成
        while stream_thread.is_alive():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error in main process: {str(e)}")
    except KeyboardInterrupt:
        print("\nProgram terminated by user")

if __name__ == "__main__":
    main()