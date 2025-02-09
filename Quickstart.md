# Levia Protocol Quickstart Guide

## Overview
Levia is an Open Source AI Metacognition & Tooling infrastructure that enables agents to recursively self-learn and optimize execution pathways. The system is designed to execute tasks rather than just provide textual responses.

## Prerequisites
- Python 3.8
- Virtual environment tool (venv, conda, etc.)

## Installation
1. Clone the repository:
``` git clone https://github.com/your-username/levia-protocol.git
 cd levia-protocol
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate`
```
3. Install dependencies:
`pip install -r requirements.txt`


## Configuration
Create a .env file in the root directory with the following required environment variable
```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url

# Azure OpenAI Configuration (if using Azure)
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_BASE_URL=your_azure_endpoint

# Database Configuration (if using MySQL)
DB_HOST=your_db_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_MAX_CONNECTIONS=10
DB_MIN_CACHED=5

# GitBook Configuration (if using documentation features)
GITBOOK_API_KEY=your_gitbook_api_key

# Azure File Server (if using file storage)
AZURE_FILE_SERVER_KEY=your_azure_storage_connection_string
```

## Running the Application
Start the main application:
```
python main.py
```
The application will initialize with available tools from the tools/ directory and start an interactive chat session.



## Core Features
1. Tool Integration: The system automatically scans and loads tools from the tools/ directory. Reference:
```
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
```

2. Memory Management: The system includes short-term memory capabilities for maintaining context during conversations. Reference:
```
class ContextStore:
    def __init__(self, max_length=5):
        """
        Initialize the context store.
        :param max_length: Maximum length of context history to maintain
        """
        self.max_length = max_length
        self.history = []

    def add(self, user_input, model_output):
        """
        Add new conversation to history.
        :param user_input: User input
        :param model_output: Model output
        """
        self.history.append({"user": user_input, "model": model_output})
        # If history exceeds max length, remove oldest entry
        if len(self.history) > self.max_length:
            self.history.pop(0)

    def get_context(self):
        """
        Get current conversation context formatted as string.
        :return: Current conversation context
        """
        context = ""
        for exchange in self.history:
            context += f"User: {exchange['user']}\n"
            context += f"Model: {exchange['model']}\n"
        return context

    def clear(self):
        """
        Clear all history.
        """
        self.history = []
```
3. Stream Processing: Supports multiple output streams including HTTP, WebSocket, and local file logging. Reference:
```
class Stream:
    """
    Stream class that manages multiple output streams.
    Supports HTTP, local file, and WebSocket output streams.
    """

    def __init__(self, stream_type="local"):
        """
        Initialize Stream with specified stream type.

        Args:
            stream_type (str): Type of stream to initialize ("http", "local", or "websocket")
        """
        self.streams = []
        if stream_type == "http":
            self.add_stream(HTTPStream("http://localhost:8000"))
        elif stream_type == "local":
            self.add_stream(LocalStream())
        elif stream_type == "websocket":
            self.add_stream(WebsocketStream("ws://localhost:8765"))
        else:
            raise ValueError(f"Invalid stream type: {stream_type}")

        # Always add log stream as secondary output
        self.add_stream(LogStream())
```
## Available Tools
The repository comes with several pre-built tools:
1. Website Scanner
2. Web Search
3. GitBook Documentation Generator
4. Location Services

## Development
To create a new tool:
1. Create a new directory in the tools/ folder
2. Create a main.py file with your tool implementation
3. Use the @simple_tool decorator to register your tool
4. Implement the required methods


Example tool structure:
```
from engine.tool_framework import simple_tool

@simple_tool("Your Tool Description")
def your_tool_method(param1, param2):
    # Tool implementation
    return result
```

## Testing
Run tests using pytest:
```
pytest test/
```

## Notes
