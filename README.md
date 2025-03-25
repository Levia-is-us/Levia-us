> [!IMPORTANT]
> Levia is currently 2 weeks old and is being worked on by a small but capable team. Thank you for being early adopters and for your patience - great things are ahead!

# Levia Protocol ([Levia.us](https://levia.us/))

Levia is an Open Source AI Metacognition & Tooling infrastructure that enables agents to recursively self-learn & optimize execution pathways.

By integrating tools and information pipelines built by its network of contributors, Levia creates a dynamic environment where agents effectively utilize real-world tools (aka **_Conductors_**). The protocol features a unique memory system that learns and improves autonomously through interaction and feedback. Levia is compatible with larger tool use paradigms such as the **Model Context Protocol**.

[Jump straight to Getting Started](#getting-started)

## Features

### Core Capabilities

- End-to-End Tool Integration: Wide variety of plugins, adapters, and API functions that enable conductors to perform actions on behalf of users and use computers, rather than telling users what to do
- Metacognition: Continuous reasoning and awareness stream
- Neuromorphic Memory Management: Hierarchical and segmented memory architecture
- Custom Query Interfaces: Support for multi-modal queries and intent understanding

### Developer Benefits

- Shared Capability Network: Access and orchestrate a growing network of tools with 100+ pre-integrated options
- Transparency: Stream reasoning and execution traces for monitoring and future optimization
- Low-Code Intent Understanding: Effortless interpretation and execution of user requests
- Simplified Pipeline Management: Abstract away pipeline upgrades, fine-tuning, and evolution - we handle that for you

### Advantages Over Traditional Frameworks

| Current Frameworks | Levia Protocol |
|-------------------|----------------|
| Difficult tool/plugin integration | Standardized formats and validation for easy integrations; autonomous tool creation through self-learning |
| Siloed runtime environments | Shared, continuously optimized workflows between agents |
| Insecure key management | Mock key calls prevent LLM leakage |

### Potential Applications

- Proactive Personal Assistance: Suggests plans without human prompting, such as recommending last-minute Valentine's gifts when you're struggling to come up with ideas while web browsing
- Boring Task Handler: Voice call agents that help with insurance claims, government fine appeals, and airline rebookings - addressing corporate inefficiencies imposed on people that persist due to bureaucracy. Levia provides a way to bypass these obstacles
- Headless Executors: Serve responses and execute tasks directly through Levia without needing to navigate through 50 different apps
- Dynamic Knowledge Tree: "Everpedia" agents aware of social trends with continuous knowledge updates, such as the latest DOGE policies, tax policies, and benefit claims, suggesting how to maximize benefits for you
- Personalized settings: Imagine having a personal negotiator (automatically handling disputes based on your latest Google Meets, negotiating bills & optimizing your budget in real-time), a personal finance optimizer (from tracking and cancelling unused $0.99 subscriptions to spotting costly non-essential purchases), or a personal daily briefer (waking up to your own information aggregator across social media, with tone tailored so precisely it feels like a dialogue between you & the world)

## Architecture

Levia's architecture mirrors human cognitive processes. Its shared memory and capability network expand with each new agent, pioneering human-like AI systems en route to sovereign AGI.

# Getting Started
## Overview
Levia is an Open Source AI Metacognition & Tooling infrastructure that enables agents to recursively self-learn and optimize execution pathways. The system is designed to execute tasks rather than just provide textual responses.

## Prerequisites
- Python 3.11 or higher
- Virtual environment tool (venv, conda, etc.)

## Installation
1. Clone the repository:
``` git clone https://github.com/your-username/levia-protocol.git
 cd Levia-us
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate`
```
3. Install dependencies:
`pip install -r requirements.txt`


## Configuration
Create a .env file in the root directory with the following required environment variables
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
### Tool Integration
The engine automatically scans and loads tools from the `tools/` directory. Here's how it works:
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

### Memory Management
The engine includes short-term memory capabilities for maintaining context during conversations:
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
### Stream Processing
The engine supports multiple output streams including HTTP, WebSocket, and local file logging:
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

The most updated tool list is found at https://levia.us

## Development Guide
To create a new tool:
1. Create a new directory in the `tools/` folder
2. Create a `main.py` file with your tool implementation
3. Use the `@run_tool` decorator to register your tool
4. Implement the required methods


Example tool structure:
```
from engine.tool_framework import simple_tool

@run_tool
class Tool_name:
    def your_tool_method(param1, param2):
        # Tool implementation
        return result
```
More details about tool development can be found in [To_build_your_tool.md](To_build_your_tool.md).

## Contributing

Join us in building the future of execution focused agents/conductors! Together, we're creating a more intelligent, proactive and capable AI ecosystem.

<p align="center">Built with ❤️ by the Levia Contributors</p>
