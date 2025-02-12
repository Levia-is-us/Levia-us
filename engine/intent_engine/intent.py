import os
from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow
from memory.short_term_memory.short_term_memory_provider.local_context_store.local_context_store import LocalContextStore

def init_tools():
    """Initialize tool registry and caller"""

    registry = ToolRegistry()
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    tools_dir = os.path.join(project_root, "tools")
    print(f"Scanning tools from: {tools_dir}")
    registry.scan_directory(tools_dir)
    return ToolCaller(registry)


def terminal_chat():
    """Start interactive chat"""
    tool_caller = init_tools()

    print("\033[93mWelcome to Levia Chat!\033[0m")
    print("Enter 'quit' to exit, 'clear' to reset current conversation")

    chat_messages = []
    while True:
        try:
            # Get user input
            user_input = input("\033[94mYou: \033[0m").strip()

            if user_input.lower() == "quit":
                print("\033[93mGoodbye!\033[0m")
                break

            if not user_input:
                continue

            reply = handle_chat_flow(chat_messages, user_input, tool_caller, "terminal")
            print("handle_chat_flow: ", reply)

        except KeyboardInterrupt:
            print("\n\033[93mProgram terminated\033[0m")
            break
        except Exception as e:
            print(f"\033[91mError occurred: {str(e)}\033[0m")


def event_chat(input_message: str, user_id: str):
    print("\033[93mWelcome to Levia Chat!\033[0m")
    tool_caller = init_tools()
    short_term_memory = LocalContextStore()
    messages = short_term_memory.get_context(user_id)
    short_term_memory.add_context({"role": "user", "content": input_message}, user_id)
    reply = handle_chat_flow(messages, input_message, tool_caller, user_id)