# Levia API Quick Start Guide

This quick start guide walks through the key steps to integrate and use the Levia HTTP Stream API.

For complete API documentation, refer to the [Levia API Documentation](https://github.com/Levia-is-us/Levia-us/tree/main/metacognitive/stream/stream_provider/http_stream).

### User ID
The `user_id` parameter is a crucial concept in this API:

*   Each `user_id` represents a unique individual user in the developer's application
*   Levia uses the `user_id` to store and differentiate chat contexts between different users
*   Developers are responsible for generating and managing unique user IDs for their user base
*   Each user's conversation history and context is isolated based on their `user_id`
*   The same `user_id` should be used consistently across sessions for the same user to maintain context

## Step 1: Register and Get API Key

1. Register for a developer account on the Levia developer platform
2. Generate an API key for your project
3. Save your API key securely - you'll need it for all API requests

## Step 2: Set Up Your Environment

```python
import requests
import json
import random
import time
import threading

# Base URL for all API requests
BASE_URL = "https://api.levia.us"

# Your API Key from Step 1
API_KEY = "your_api_key_here"

# Headers for API requests
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
```

## Step 3: Create a Chat Session

Each user in your application needs a chat session to interact with Levia.

```python
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
            f"{BASE_URL}/levia/chat/create",
            json={"user_id": user_id},
            headers=headers
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

# Example: Create a session for user "user123"
session_id = create_chat_session("user123")
print(f"Created session: {session_id}")
```

## Step 4: Send a Chat Message

Send a message and get a request ID for streaming the response.

```python
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
            f"{BASE_URL}/levia/chat",
            json={
                "user_id": user_id,
                "intent": message,
                "session_id": session_id
            },
            headers=headers
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

# Example: Send a message
message = "What is the capital of France?"
request_id = send_chat_message("user123", message, session_id)
print(f"Message sent, request ID: {request_id}")
```

## Step 5: Stream the Response

Use Server-Sent Events (SSE) to receive the streaming response.

```python
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
            url = f"{BASE_URL}/levia/chat/stream/{request_id}"
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

# Example: Connect to the stream
stream_thread = connect_to_stream(request_id)

# Keep the main thread alive while the stream is processing
print("Waiting for response...")
while stream_thread.is_alive():
    time.sleep(0.1)
```

## Step 6: Handle Reconnections (Optional)

If a client disconnects, you can retrieve the current request ID for a user.

```python
def get_active_request(user_id):
    """
    Check if there's an active request for a user
    
    Args:
        user_id (str): The user's ID
        
    Returns:
        str or None: Request ID if active, None otherwise
    """
    try:
        response = requests.get(
            f"{BASE_URL}/levia/chat/request/{user_id}",
            headers=headers
        )
        
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

# Example: Check if user has an active request
active_request = get_active_request("user123")
if active_request:
    print(f"Reconnecting to request: {active_request}")
    stream_thread = connect_to_stream(active_request)
```

## Step 7: Put It All Together

Here's a complete example integrating all the steps:

```python
def main():
    """Main function to demonstrate HTTP Stream API usage"""
    try:
        print("Starting HTTP Stream API client...")
        
        # Configuration
        user_id = f"user_{random.randint(1000, 9999)}"
        user_message = "Tell me about quantum computing"
        
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
        
        while stream_thread.is_alive():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error in main process: {str(e)}")
    except KeyboardInterrupt:
        print("\nProgram terminated by user")

if __name__ == "__main__":
    main()
```

## Next Steps

- Implement error handling and retries
- Store session IDs in your database to maintain conversations
- Create a user interface to display streaming responses
- Implement user authentication in your application
- Explore advanced features and configurations