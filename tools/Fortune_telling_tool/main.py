import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework import run_tool, BaseTool
from engine.llm_provider.llm import chat_completion
from tools.Fortune_telling_tool.fortune_telling_prompt import get_fortune_telling_prompt

@run_tool("FortuneTellingTool")
class FortuneTellingTool(BaseTool):
    """Tool for fortune telling based on birth date"""
    
    def fortune_telling(self, user_concern: dict) -> dict:
        """
        Provide fortune telling based on user's birth date
        
        Args:
            user_concern (dict): User message containing birth date information
            
        Returns:
            dict: Fortune telling result and advice
        """

        prompt = get_fortune_telling_prompt(user_concern)
        response = chat_completion(
            prompt,
            model="deepseek-r1",
            config={"temperature": 0.7},
        )
        try:
            # Your fortune telling logic here
            return {
                "status": "success",
                "result": response
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            } 