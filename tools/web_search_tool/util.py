import time
from aipolabs import Aipolabs
from engine.llm_provider.llm import chat_completion
from aipolabs.types.functions import FunctionExecutionResult
from aipolabs._exceptions import ServerError
import os

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
FAST_MODEL_NAME = os.getenv("FAST_MODEL_NAME")


def generate_search_keywords(intent: str):
    """
    This function is used to generate search keywords from user intent.
    Args:
        intent (str): The intent of the user.
    Returns:
        search keywords.
    """

    # Generate search keywords through LLM
    prompt = """
    You will be given a user’s input as a string. Your task is to extract the most appropriate search keywords based on the given input. The output should be a list of keywords, and you should generate as few keywords as possible while ensuring they are concise and accurately reflect the user's need. 

    The keywords may consist of multiple related terms, but avoid unnecessary or redundant words.

    Examples:

    1. Input: The user wants to learn how to use MySQL.
    Output: ["SQL usage guide"]


    2. Input: The user wants to know about the economic trends in China for 2025.
    Output: ["2025 China economic forecast"]


    3. Input: The user wants to learn how to analyze data with Python.
    Output: ["Python data analysis"]


    4. Input: The user wants to learn how to improve work efficiency.
    Output: ["work efficiency"]


    5. Input: The user wants to know about stock market trends and investment advice for 2025 in the U.S.
    Output: ["2025 U.S. stock market trends"]


    Your task:
    - Extract only the most relevant and minimal keywords from the input.
    - The keywords should accurately reflect the search query, and as few keywords as necessary to do so.
    - Ensure clarity and avoid redundancy.
    - The output should be only the keywords, no other text.
    """

    try:
        output = chat_completion(
            [
                {"role": "assistant", "content": prompt},
                {"role": "user", "content": intent},
            ],
            model=QUALITY_MODEL_NAME,
            config={"temperature": 0.7},
        )
        keywords = eval(output)
    except Exception as e:
        print(f"Generate search keywords error: {str(e)}")
        keywords = []
    return keywords


def extract_relevance_url(intent: str, content_list: str) -> list:
    """
    This function is used to generate the relevance URLs from the search results.
    Args:
        intent (str): The intent of the user.
        content_list (str): The search results.
    Returns:
        The relevance URLs.
    """
    prompt = """
    Given a user intent and a list of search results, select 1-3 most relevant URLs.
    
    Requirements:
    1. Analyze the relevance between each result and the user intent
    2. Consider content freshness and authority
    3. Select only the most relevant 1-3 URLs
    4. Ignore results that are:
       - Spam or low quality content
       - Not directly related to the intent
       - Duplicate information
    5. The output should be only the urls, no other text.

    Input format:
    intent: <user intent>
    content_list: <search results>
    
    Output format:
    [url1, url2, url3]
    """
    try:
        output = chat_completion(
            [
                {"role": "assistant", "content": prompt},
                {
                    "role": "user",
                    "content": f"Intent: {intent}\nContent List: {content_list}",
                },
            ],
            model=QUALITY_MODEL_NAME,
            config={"temperature": 0.7},
        )
        urls = eval(output)
    except Exception as e:
        print(f"Extract relevance url error: {str(e)}")
        urls = []
    return urls


def aipolabs_search(client: Aipolabs, keyword: str):
    """
    Function to search for a given keyword using the Aipolabs client, with retry logic in case of errors.

    Args:
        client (Aipolabs): The Aipolabs client that will execute the function.
        keyword (str): The search term or keyword to be used in the search query.

    Returns:
        FunctionExecutionResult: The result of the function execution, containing the search results or any errors.
    """
    retries = 3  # Maximum number of retries
    attempt = 0  # Track the number of attempts

    while attempt < retries:
        try:
            # Execute the search function using the Aipolabs client
            result: FunctionExecutionResult = client.functions.execute(
                function_name="TAVILY__SEARCH",
                function_parameters={"body": {"query": keyword}},
            )

            return result

        except ServerError as e:
            # Handle known errors by retrying up to 3 times
            attempt += 1
            if attempt < retries:
                print(f"Error occurred: {e}. Retrying... ({attempt}/{retries})")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                print(f"Max retries reached. Error: {e}")
                raise  # Reraise the error after max retries
