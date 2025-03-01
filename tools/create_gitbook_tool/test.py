import os
import sys


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller


def main():
    registry = ToolRegistry()
    
    # Use absolute path
    tools_dir = os.path.join(project_root, "tools")
    registry.scan_directory(tools_dir)  # Scan tools directory

    # Create ToolCaller instance
    caller = ToolCaller(registry)

    markdown_text =  """
### Key Physics Breakthroughs and Upcoming Events
1. **Recent Physics Breakthroughs:**
   - **Multipartite Entanglement:** Achieved on an optical chip, paving the way for scalable quantum information systems.
1. **Recent Physics Breakthroughs:**
   - **Multipartite Entanglement:** Achieved on an optical chip, paving the way for scalable quantum information systems.
   - **Multipartite Entanglement:** Achieved on an optical chip, paving the way for scalable quantum information systems.
   - **Quantum Properties Detection:** A new method inspired by Maxwell's demon uses heat flow to detect quantum properties without direct measurements.
   - **Superconductivity Innovations:** Resilient superconducting fluctuations in atomically thin NbSe2 materials have been uncovered, enhancing our understanding of superconductivity.
   - **Plasma Physics Advancement:** A deep-learning model enhances plasma predictions in nuclear fusion by 1,000 times, showcasing AI's role in accelerating complex research.

2. **Upcoming Events:**
   - The **2025 APS Global Physics Summit** will be held from March 16-21 in Anaheim, California, expecting over 14,000 participants. The summit will feature presentations from students and professionals, with both in-person and virtual attendance options available.

For more detailed insights, you can check out the compiled document here: [Key Physics Breakthroughs and Upcoming Events](https://hpps-organization.gitbook.io/cornjames/Key_Physics_Breakthroughs).

Feel free to reach out if you need anything else or further information on specific topics!
"""
    result = caller.call_tool(tool_name="SaveMarkdownToGitbook", method="save_markdown_to_gitbook", kwargs={"content":markdown_text})
    
    if result:
        if "error" in result:

            print(f"Tool execution error: {result['error']}")
        else:
            print(f"response info: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()

