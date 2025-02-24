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
            "fdv_in_usd": "100", // the fdv of the token in usd
            "market_cap_in_usd": "100", // the market cap of the token in usd
            "pool_creation_date": "2021-01-01", // the creation date of the pool
            "reserve_in_usd": "100", // the reserve of the token in usd
            "twitter_url": "https://x.com/example" // the twitter url of the token
        }
    """
    def get_token_info(self, token_address: str):
        pool = None
        twitter_url = ''
        try:
            pool = get_token_pool_info(token_address)
            if pool is None:
                return 'not found token info'
        except Exception as e:
            return 'not found token info'
        
        try:
            twitter_url = get_token_twitter_url(pool, pool['address'])
        except Exception as e:
            pass

        return {
            "price_in_usd":pool['price_in_usd'],
            "fdv_in_usd":pool['fdv_in_usd'],
            "market_cap_in_usd":pool['market_cap_in_usd'],
            "pool_creation_date":pool['pool_creation_date'],
            "reserve_in_usd":pool['reserve_in_usd'],
            "twitter_url":twitter_url
        }
        

