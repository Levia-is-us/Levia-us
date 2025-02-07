from openai import OpenAI
import os
from dotenv import load_dotenv

def setup_openai_client():
    """Setup OpenAI client with configuration"""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url:
        print("\033[93mWarning: OPENAI_BASE_URL not found in .env file\033[0m")
        
    return OpenAI(api_key=api_key, base_url=base_url)