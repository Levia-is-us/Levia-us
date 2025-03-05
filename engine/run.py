# from engine.intent_engine.intent import ChatClient
from engine.intent_engine.intent_terminal import terminal_chat
from memory.plan_memory.plan_memory import PlanContextMemory
from engine.intent_engine.intent_event import event_chat
import os
from metacognitive.stream.stream_provider.http_stream.http_stream import HTTPStream

http_stream = HTTPStream(port=7072)

app = http_stream.app

INTERACTION_MODE = os.environ.get("INTERACTION_MODE", "terminal")
planContext = PlanContextMemory()

def run():
    if INTERACTION_MODE == "terminal":
        terminal_chat()
    elif INTERACTION_MODE == "server":
        app.run(host="0.0.0.0", port=7072, threaded=True)

__all__ = ['run']
