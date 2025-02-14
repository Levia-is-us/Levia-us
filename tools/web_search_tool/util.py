import json
import re
import time
import os
from aipolabs import Aipolabs
from aipolabs.types.functions import FunctionExecutionResult
from aipolabs._exceptions import ServerError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from engine.llm_provider.llm import chat_completion

QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
PERFORMANCE_MODEL_NAME = os.getenv("PERFORMANCE_MODEL_NAME")


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
            config={"temperature": 0.5},
        )
        keywords = eval(output)
    except Exception as e:
        print(f"Generate search keywords error: {str(e)}")
        keywords = []
    return keywords


def extract_relevance_url(intent: str, contents: str) -> list:
    """
    This function is used to generate the relevance URLs from the search results.
    Args:
        intent (str): The intent of the user.
        contents (str): The search results.
    Returns:
        The relevance URLs.
    """
    prompt = """
    Given a user intent and search results, select 1-3 most relevant URLs.

    Requirements:
    1. Analyze the relevance between each result and the user intent
    2. Consider content freshness and authority
    3. Select only the most relevant 1-3 URLs
    4. Ignore results that are:
        - Spam or low quality content
        - Not directly related to the intent
        - Duplicate information
        - URLs from video/audio hosting sites (e.g. youtube.com, vimeo.com, soundcloud.com)
    5. The output should be only the URL list, no other text ( eg. ["url1", "url2", "url3"])

    Input format:
    intent: <user intent>
    contents: url: <url1> content:<content1>
            url: <url2> content:<content2>
            url: <url3> content:<content3>

    Output format:
    ["url1", "url2", "url3"]
    """
    try:
        output = chat_completion(
            [
                {"role": "assistant", "content": prompt},
                {
                    "role": "user",
                    "content": f"Intent: {intent}\nContents: {contents}",
                },
            ],
            model=QUALITY_MODEL_NAME,
            config={"temperature": 0.7},
        )
        # Try to parse JSON directly from output
        try:
            # If output is a dictionary string containing JSON
            result_dict = json.loads(output)
            if isinstance(result_dict, dict) and "result" in result_dict:
                return result_dict["result"]
        except json.JSONDecodeError:
            pass

        # If direct parsing fails, try to extract URL list
        match = re.search(r"(\[.*?\])", output.replace("\n", ""))
        if match:
            try:
                urls = json.loads(match.group(1))
                return urls
            except json.JSONDecodeError:
                print("Failed to parse URL list from matched pattern")
                return []

        return []
    except Exception as e:
        print(f"Extract relevance url error: {str(e)}")
        return []


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
    client = Aipolabs(api_key=os.environ.get("AIPOLABS_API_KEY"))

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
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            """
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


def safe_get_element(elements, index=0):
    """
    Safely get element from list with index checking.

    Args:
        elements (list): List of web elements
        index (int): Index to retrieve

    Returns:
        WebElement or None if not found
    """
    return elements[index] if elements and len(elements) > index else None


def extract_element_content(element, tag_name, attr=None):
    """
    Extract content from element with safety checks.

    Args:
        element: Parent web element
        tag_name (str): HTML tag to find
        attr (str): Attribute to extract, if None returns text

    Returns:
        str: Extracted content or empty string
    """
    elements = element.find_elements(By.TAG_NAME, tag_name)
    found_elem = safe_get_element(elements)
    if found_elem is None:
        return ""

    return (
        found_elem.get_attribute(attr) if attr else found_elem.text.replace("\n", " ")
    )


def extract_search_result(element):
    """
    Extract URL and summary from a search result element.

    Args:
        element: Search result web element

    Returns:
        tuple: (url, summary)
    """
    url = extract_element_content(element, "a", "href")
    summary = " ".join(
        elem.text.replace("\n", " ")
        for elem in element.find_elements(By.TAG_NAME, "span")
        if elem.text
    )
    return url, summary


def handle_search_results(search_results: list) -> list:
    """
    Extract URLs and content from search results and return formatted strings.

    Args:
        search_results: List of search result elements

    Returns:
        list: Formatted strings with URLs and content
    """
    content_list = []

    if len(search_results) > 3:
        # Remove the second search result with no contents
        search_results.remove(search_results[1])

        # Process remaining results
        results = [extract_search_result(elem) for elem in search_results]
        urls, summaries = zip(*[r for r in results if r[0]])  # Filter out empty URLs

    else:
        # Process first result
        first_url, first_summary = extract_search_result(search_results[0])

        # Process remaining results
        other_results = search_results[1]
        child_divs = other_results.find_elements(By.CSS_SELECTOR, ":scope > div")
        other_results = [extract_search_result(elem) for elem in child_divs]

        # Combine results
        urls = [first_url] + [url for url, _ in other_results if url]
        summaries = [first_summary] + [
            summary for _, summary in other_results if summary
        ]

    # Format results
    content_list.extend(
        [
            f"url: {url} content: {summary}"
            for url, summary in zip(urls, summaries)
            if url and summary
        ]
    )

    return content_list


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
    # Set the explicit wait time
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
                # Type keyword in the search box
                search_box.click()
                search_box.send_keys(keyword)
                search_box.send_keys(Keys.RETURN)
                # Wait for the search results container to be visible
                search_rets = wait.until(
                    EC.visibility_of_element_located((By.ID, "rso"))
                )
                # Scroll down to simulate user browsing behavior
                scroll_to_bottom(driver)
                # Retrieve individual search result elements
                search_results = search_rets.find_elements(
                    By.CSS_SELECTOR, ":scope > div"
                )
                # time.sleep(60000)
                # Extract URLs and content from search results
                contents = handle_search_results(search_results)
                content_list.extend(contents)
            except Exception as err:
                print(f"Extract google search output error for '{keyword}': {err}")
    finally:
        driver.quit()

    return content_list
