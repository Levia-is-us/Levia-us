import time
import os
import pyautogui
from aipolabs import Aipolabs
from aipolabs.types.functions import FunctionExecutionResult
from aipolabs._exceptions import ServerError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from engine.llm_provider.llm import create_chat_completion
from dotenv import load_dotenv
import ast

project_root = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")
AIPOLABS_API_KEY = os.getenv("AIPOLABS_API_KEY")



def generate_search_keywords(intent: str) -> list:
    """
    This function is used to generate search keywords from user intent.
    Args:
        intent (str): The intent of the user.
    Returns:
        search keywords.
    """

    # Generate search keywords through LLM
    prompt = """
    You will be given a user's input as a string. Your task is to extract the most appropriate search keywords based on the given input. The output should be a list of keywords, and you should generate as few keywords as possible while ensuring they are concise and accurately reflect the user's need. 

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
        output = create_chat_completion(
            system_prompt = prompt,
            model=PERFORMANCE_MODEL_NAME,
            prompt=intent,
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
    ["url1", "url2", "url3"]
    """
    try:
        output = create_chat_completion(
            system_prompt = prompt,
            model=PERFORMANCE_MODEL_NAME,
            prompt=f"Intent: {intent}\nContent List: {content_list}",
            config={"temperature": 0.7},
        )
        if output == []:
            urls = "No results found."
        else:
            urls = eval(output)
    except Exception as e:
        print(f"Extract relevance url error: {str(e)}")
        raise Exception("No output from the model")
    return urls


def aipolabs_search(client: Aipolabs, keyword: str) -> FunctionExecutionResult:
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


def search_non_visual(keywords: list) -> list:
    """
    This function is used to perform non-visual web searches for information.

    Args:
        keywords (list): The list of search keywords.
    Returns:
        A list of URLs and content that match the intent.
    """
    # Initialize search engine
    client = Aipolabs(api_key=AIPOLABS_API_KEY)

    content_list = []
    for keyword in keywords:
        try:
            # Search for each keyword
            result: FunctionExecutionResult = aipolabs_search(client, keyword)
            # Extract content from search results
            contents = [
                f'url: {result["url"]} content: {result["content"]}'
                for result in result.data["results"]
            ]
            content_list.extend(contents)
        except Exception as e:
            print(f"Aipolabs search error: {str(e)}")

    return content_list


def init_driver() -> webdriver.Chrome:
    """Initialize and return a configured Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    )
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        },
    )
    driver.maximize_window()
    return driver


def scroll_to_bottom(driver, duration=5.0) -> None:
    """
    Scroll the page to the bottom; duration specifies the total scroll time.

    Args:
        driver: The WebDriver instance
        duration: The total duration of the scroll operation in seconds

    Returns:
        None
    """
    total_height = driver.execute_script("return document.body.scrollHeight")
    step_time = 0.01
    steps = max(1, int(duration / step_time))  # Ensure at least one scroll step
    step_height = total_height / steps
    for i in range(steps):
        driver.execute_script(f"window.scrollTo(0, {(i + 1) * step_height});")
        time.sleep(step_time)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def human_like_google_search(keyword, type_interval=0.1) -> None:
    """
    Perform a Google search with a delay between keystrokes to simulate human input

    Args:
        keyword: The search keyword
        type_interval: The interval between keystrokes

    Returns:
        None
    """

    # Type the keyword with a delay between keystrokes to simulate human input
    pyautogui.typewrite(keyword, interval=type_interval)


def search_visual(keywords: list) -> list:
    """
    Perform a visual search using specified keywords and return the matching URLs with content.

    Args:
        keywords: A list of keywords to search for.

    Returns:
        A list of strings, each containing the URL and content of a search result.
    """
    # Initialize the Chrome WebDriver
    driver = init_driver()
    wait = WebDriverWait(driver, 30)
    content_list = []

    try:
        for keyword in keywords:
            try:
                # Navigate to Google's homepage
                driver.get("https://www.google.com")
                # Wait until the search box is clickable
                search_box = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#APjFqb"))
                )
                # Simulate human-like typing of the search keyword
                human_like_google_search(keyword)
                search_box.send_keys(Keys.RETURN)
                # Wait for the search results container to be visible
                search_results = wait.until(
                    EC.visibility_of_element_located((By.ID, "rso"))
                )
                # Retrieve individual search result elements
                search_results = search_results.find_elements(
                    By.CSS_SELECTOR, ":scope > div"
                )
                # Extract URL and summary from the first search result
                first_elem = search_results[0]
                first_url_elem = first_elem.find_elements(By.TAG_NAME, "a")[0]
                first_url = first_url_elem.get_attribute("href")
                first_summary_elems = first_elem.find_elements(By.TAG_NAME, "span")
                first_summary = " ".join(
                    [summary_elem.text for summary_elem in first_summary_elems]
                )
                # Scroll down to simulate user browsing behavior
                scroll_to_bottom(driver)
                # Extract remaining search results from subsequent elements
                other_results = search_results[1]
                child_divs = other_results.find_elements(
                    By.CSS_SELECTOR, ":scope > div"
                )
                other_url_elems = [
                    elem.find_elements(By.TAG_NAME, "a")[0] for elem in child_divs
                ]
                other_summary_elems = [
                    elem.find_elements(By.TAG_NAME, "span")[0] for elem in child_divs
                ]
                urls = [first_url] + [
                    elem.get_attribute("href") for elem in other_url_elems
                ]
                summaries = [first_summary] + [
                    elem.text for elem in other_summary_elems
                ]
                # Build and extend the content list with the result details
                content_list.extend(
                    [f"url: {u} content: {s}" for u, s in zip(urls, summaries)]
                )
            except Exception as err:
                print(f"Extract google search output error for '{keyword}': {err}")
    finally:
        driver.quit()

    return content_list
