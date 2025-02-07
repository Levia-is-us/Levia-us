import os
import sys
import dotenv
import websockets

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from metacognative.stream.stream import Stream
import asyncio

# test for local stream
stream = Stream(stream_type="local")
stream.output("test")
stream.output("test2")

# # test for http stream
# stream = Stream(stream_type="http")
# stream.output("test")
# stream.output("test2")


# # test for websocket stream
async def test_websocket_send():
    count = 1
    while True:
        try:
            stream.output(f"test-stream {count}")
            print(f"send message: {count}")
            count += 1
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Error sending log: {e}")
            await asyncio.sleep(3)  # Wait before retrying
            
async def test_websocket_receive():
    # Add delay to allow server to start first
    await asyncio.sleep(2)
    print("start receive")
    while True:
        try:
            # Use websockets library instead of websocket-client for async support
            async with websockets.connect("ws://localhost:3000") as ws:
                try:
                    while True:
                        message = await ws.recv()
                        print(f"receive message: {message}")
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
        except Exception as e:
            print(f"Websocket connection error: {e}")
            await asyncio.sleep(1)  # Wait before retrying

# Initialize stream
stream = Stream(stream_type="websocket")
# Run sender and receiver concurrently
print("Starting sender and receiver...")

async def main():
    await asyncio.gather(test_websocket_send(), test_websocket_receive())


asyncio.run(main())
