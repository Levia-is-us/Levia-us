# from engine.intent_engine.intent import ChatClient
from engine.intent_engine.intent import terminal_chat
from memory.plan_memory.plan_memory import PlanContextMemory

planContext = PlanContextMemory()

def run():
    terminal_chat()

__all__ = ['run']