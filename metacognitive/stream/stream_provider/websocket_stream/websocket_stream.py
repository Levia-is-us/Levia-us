import asyncio
import websockets
from metacognitive.stream.stream_provider.base_stream import BaseStream
from urllib.parse import urlparse
import threading


class WebsocketStream(BaseStream):
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.server = None
        self.clients = set()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        threading.Thread(target=self.start_server, daemon=True).start()

    async def handler(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)

    def start_server(self):
        async def main():
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

    def output(self, log: str):
        try:
            if self.server and self.clients:

                async def broadcast():
                    if self.server and self.clients:
                        websockets.broadcast(self.clients, log)
                    else:
                        print("WebsocketStream server or clients not found")

                asyncio.run_coroutine_threadsafe(broadcast(), self.loop)
        except Exception as e:
            print(f"WebsocketStream broadcast error: {e}")
