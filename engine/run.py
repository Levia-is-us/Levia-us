# from engine.intent_engine.intent import ChatClient
from engine.intent_engine.intent_terminal import terminal_chat
from memory.plan_memory.plan_memory import PlanContextMemory
from engine.intent_engine.intent_event import event_chat
import os


INTERACTION_MODE = os.environ.get("INTERACTION_MODE", "terminal")
planContext = PlanContextMemory()

def run():
    if INTERACTION_MODE == "terminal":
        terminal_chat()
    else:
        event_chat()

__all__ = ['run']
