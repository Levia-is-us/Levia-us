import os
from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller
from engine.flow.chat_handler_flow.chat_handler_flow import handle_chat_flow


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


def chat():
    """Start interactive chat"""
    tool_caller = init_tools()

    print("\033[93mWelcome to OpenAI Chat Program!\033[0m")
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

            reply = handle_chat_flow(chat_messages, user_input, tool_caller)
            print("handle_chat_flow: ", reply)

        except KeyboardInterrupt:
            print("\n\033[93mProgram terminated\033[0m")
            break
        except Exception as e:
            print(f"\033[91mError occurred: {str(e)}\033[0m")
