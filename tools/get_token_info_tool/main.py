import sys
import os

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from engine.tool_framework import run_tool, BaseTool
from tools.get_token_info_tool.utils import  get_token_pool_info, get_token_twitter_url



@run_tool
class GetTokenInfoTool(BaseTool):
    """
    This tool get the new token info from the token address.
    Args:
        token_address (str): The token address.
    Returns:
        a json about the token info details.
        {
            "price_in_usd": "100", // the price of the token in usd
            "twitter_url": "https://x.com/example" // the twitter url of the token
        }
    """
    def get_token_info(self, token_address: str):
        pool = None
        try:
            pool = get_token_pool_info(token_address)
        except Exception as e:
            return 'not found token info'
        
        twitter_url = get_token_twitter_url(pool, pool['address'])
        return {"price_in_usd":pool['price_in_usd'], "twitter_url":twitter_url}
        

