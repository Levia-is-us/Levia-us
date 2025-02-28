import asyncio
import websockets
from metacognitive.stream.stream_provider.base_stream import BaseStream
from urllib.parse import urlparse
import threading
from concurrent.futures import ThreadPoolExecutor


class WebsocketStream(BaseStream):
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.server = None
        # Store clients in dictionary with user_id as key and websocket connection as value
        self.clients = {}
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        threading.Thread(target=self.start_server, daemon=True).start()

    async def handler(self, websocket):
        from engine.intent_engine.intent_event import event_chat
        import json
        import asyncio
        executor = ThreadPoolExecutor(max_workers=100)
        try:
            async for message in websocket:
                try:
                    try:
                        message_data = json.loads(message)
                    except:
                        message_data = eval(message)
                    
                    user_id = message_data.get('uid')
                    content = message_data.get('content')
                    
                    if user_id:
                        self.clients[user_id] = websocket
                        asyncio.create_task(
                            self.process_message(user_id, content, executor)
                        )
                    else:
                        print("No user_id found in message")
                except Exception as e:
                    print(f"Invalid message format: {message}, error: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosed:
            for uid, ws in list(self.clients.items()):
                if ws == websocket:
                    print(f"Connection closed for user {uid}")
                    del self.clients[uid]
                    break

    async def process_message(self, user_id: str, content: str, executor: ThreadPoolExecutor):
        from engine.intent_engine.intent_event import event_chat
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            executor, 
            lambda: event_chat(user_id=user_id, input_message=content)
        )

    def start_server(self):
        async def main():
            print(f"WebsocketStream server starting on {self.ws_url}")
            parsed_url = urlparse(self.ws_url)
            host = parsed_url.hostname or "localhost"
            port = parsed_url.port or 8760

            async with websockets.serve(self.handler, host, port) as server:
                self.server = server
                await server.serve_forever()

        try:
            self.loop.run_until_complete(main())
        except Exception as e:
            print(f"WebsocketStream server error: {e}")
            self.server = None

    def output(self, log: str, user_id: str, type: str, child_id: str = ""):
        message = {
            "log": log,
            "user_id": user_id,
            "type": type,
            "child_id": child_id
        }
        log = str(message)
        try:
            async def send_message():
                if user_id in self.clients:
                    await self.clients[user_id].send(log)
                else:
                    # print(f"WebsocketStream client connection not found for user {user_id}")
                    pass
                    # print(f"Client connection not found for user {user_id}")
            asyncio.run_coroutine_threadsafe(send_message(), self.loop)
        except Exception as e:
            print(f"WebsocketStream send error: {e}")
