import os
import requests
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

def find_token_by_token_name(tokens, token_name):
    for token in tokens:
        if token['attributes']['name'] == token_name:
            return token
    return None 

def find_pool_by_volume(pools):
    return max(pools, key=lambda pool: float(pool['from_volume_in_usd']), default=None)

def get_token_pool_info(token_address: str) -> dict:
    result = get_request('https://app.geckoterminal.com/api/p1/search?query='+token_address)
    pool = find_pool_by_volume(result['data']['attributes']['pools'])
    return pool

def get_token_twitter_url(pool: dict, token_address: str) -> str:
    try:
        params = '?include=tokens'
        twitter_result = get_request('https://app.geckoterminal.com/api/p1/'+pool['network']['identifier']+'/pools/'+token_address+params)
        target_token = find_token_by_token_name(twitter_result['included'], pool['tokens'][1]['name'])
        links = target_token['attributes']['links']
        twitter_url ='https://x.com/'+links['twitter_handle']
        return twitter_url
    except Exception as e:
        return ''


def get_request(url: str) -> dict:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"request error: {e}")
        return {}