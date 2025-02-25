import os
import sys
import dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller


def main():
    registry = ToolRegistry()
    tools_dir = os.path.join(project_root, "tools")
    registry.scan_directory(tools_dir)

    caller = ToolCaller(registry)
    result = caller.call_tool(
        tool_name="WebsiteScanTool",
        method="website_scan",
        kwargs={
            "url_list": [{'url': 'https://edition.cnn.com/', 'summary': 'Breaking news and latest updates (3 hours old) covering U.S., world, weather, entertainment, politics, and health from a globally recognized news authority.'}, {'url': 'https://www.bbc.com/news/world', 'summary': "International news updates (6 hours old) featuring Macron's remarks on Ukraine-Russia negotiations and European diplomacy, from a trusted global news source."}, {'url': 'https://news.yahoo.com/', 'summary': 'Breaking news (2 hours old) including U.S. diplomatic developments at the UN and critical health alerts about a deadly listeria outbreak linked to nutritional shakes.'}],
            "intent": "What is Levia,and how it works?"
        }
    )

    if result:
        if "error" in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"Success: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()