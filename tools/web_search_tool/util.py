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
from engine.utils.json_util import extract_json_from_str
QUALITY_MODEL_NAME = os.getenv("QUALITY_MODEL_NAME")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")


def generate_search_keywords(intent: str) -> list:
    """
    This function is used to generate search keywords from user intent.
    Args:
        intent (str): The intent of the user.
    Returns:
        search keywords.
    """

    # Generate search keywords through LLM
    prompt = """You are an advanced keyword extraction system designed to help users optimize their search queries. Your task is to analyze a given user input and generate 1-3 concise, relevant keywords that accurately reflect the user's search intent. These keywords should be suitable for use in search engines to find the most relevant information.

Here is the user's intent:

<user_intent>
{USER_INTENT}
</user_intent>

Please follow these steps to generate the keywords:

1. Analyze the user's input to identify the main topic and any specific attributes (such as time, location, or context).
2. Extract the most relevant concepts and terms.
3. Combine related terms and remove unnecessary words to create concise keywords.
4. Ensure that the keywords accurately reflect the user's search intent.
5. Generate between 1 and 3 keywords, with fewer being preferable if they can capture the essence of the query.

Your final output should be a list of 1-3 keywords, each enclosed in quotes and surrounded by square brackets. For example:

["keyword 1", "keyword 2", "keyword 3"]

or

["single keyword"]

Remember, the goal is to create keywords that will help the user find the most relevant information when used in a search engine.
"""
    try:
        prompt = prompt.format(USER_INTENT=intent)
        output = chat_completion(
            [
                {"role": "user", "content": prompt},
            ],
            model=CHAT_MODEL_NAME,
            config={"temperature": 0.5},
        )
        print(f"Generate search keywords output: {output}")

        try:
            keywords = extract_json_from_str(output)
            if not isinstance(keywords, list):
                print("Invalid keywords format: expected list")
                return []
        except json.JSONDecodeError as json_err:
            print(f"Failed to parse keywords")
            return []

        return keywords
    except Exception as e:
        print(f"Generate search keywords error: {str(e)}")
        return []


def extract_relevance_url(intent: str, contents: str) -> list:
    """
    This function is used to generate the relevance URLs from the search results.
    Args:
        intent (str): The intent of the user.
        contents (str): The search results.
    Returns:
        The relevance URLs.
    """
    prompt = """You are an advanced search result curator tasked with selecting the most relevant URLs from a list of search results based on a given user intent. Your goal is to provide 1-3 high-quality, relevant results that best match the user's needs.

Here is the user's search intent:
<user_intent>
{USER_INTENT}
</user_intent>

And here is the list of search results:
<search_results>
{SEARCH_RESULTS}
</search_results>

Please follow these steps to select the most appropriate URLs:

1. Analyze the relevance of each search result to the user intent.
2. Consider the freshness and authority of the content.
3. Select only the 1-3 most relevant URLs that meet the following criteria:
   - Directly related to the user intent
   - Not spam or low-quality content
   - Not duplicate information
   - Not from video/audio hosting sites (e.g., youtube.com, vimeo.com, soundcloud.com)

After your evaluation, provide your final selection in the following JSON format:

[
  "selected_url_1",
  "selected_url_2",
  "selected_url_3"
]

Note that you may select fewer than 3 URLs if there aren't enough high-quality, relevant results that meet the criteria. The minimum is 1 URL, and the maximum is 3 URLs.

Please begin your evaluation now, followed by your final selection in the specified JSON format without any other text.
    """
    try:
        prompt = prompt.format(USER_INTENT=intent, SEARCH_RESULTS=str(contents))
        output = chat_completion(
            [
                {"role": "user", "content": prompt},
            ],
            model=CHAT_MODEL_NAME,
            config={"temperature": 0.7},
        )
        # Try to parse JSON directly from output
        try:
            # If output is a dictionary string containing JSON
            result_dict = extract_json_from_str(output)
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


def process_multiple_results(search_results):
    """
    Process search results when there are more than 3 results.

    Args:
        search_results: List of search result elements

    Returns:
        tuple: Lists of URLs and summaries
    """
    results = [extract_search_result(elem) for elem in search_results]
    filtered_results = [r for r in results if r[0]]
    if not filtered_results:
        return [], []
    urls, summaries = zip(*filtered_results)
    return list(urls), list(summaries)


def process_dual_results(search_results):
    """
    Process search results when there are 2 results.

    Args:
        search_results: List containing two search result elements

    Returns:
        tuple: Lists of URLs and summaries
    """
    # Extract URLs and summaries from the first result
    first_url, first_summary = extract_search_result(search_results[0])

    # Extract URLs and summaries from the other result
    other_results = search_results[1]
    child_divs = other_results.find_elements(By.CSS_SELECTOR, ":scope > div")
    other_results = [extract_search_result(elem) for elem in child_divs]

    urls = [first_url] + [url for url, _ in other_results if url]
    summaries = [first_summary] + [summary for _, summary in other_results if summary]

    return urls, summaries


def process_single_result(search_result):
    """
    Process a single search result.

    Args:
        search_result: Single search result element

    Returns:
        tuple: Lists of URLs and summaries
    """
    try:
        search_tab = search_result.find_element(By.CSS_SELECTOR, "#kp-wp-tab-overview")
        child_divs = search_tab.find_elements(By.CSS_SELECTOR, ":scope > div")
        results = [extract_search_result(elem) for elem in child_divs]
        filtered = [r for r in results if r[0]]
        if not filtered:
            return [], []
        urls, summaries = zip(*filtered)
        return list(urls), list(summaries)
    except Exception as e:
        print(f"Error processing single result: {e}")
        return [], []


def handle_search_results(search_results: list) -> list:
    """
    Extract URLs and content from search results and return formatted strings.

    Args:
        search_results: List of search result elements

    Returns:
        list: Formatted strings with URLs and content
    """
    length = len(search_results)

    try:
        if length > 3:
            urls, summaries = process_multiple_results(search_results)
        elif length > 1:
            urls, summaries = process_dual_results(search_results)
        elif length == 1:
            urls, summaries = process_single_result(search_results[0])
        else:
            return []

        return [
            f"url: {url} content: {summary}"
            for url, summary in zip(urls, summaries)
            if url and summary
        ]

    except Exception as e:
        print(f"Error handling search results: {e}")
        return []


def search_visual(keywords: list) -> list:
    """
    Perform a visual search using specified keywords and return the matching URLs with content.

    Args:
        keywords: A list of keywords to search for.

    Returns:
        A list of strings, each containing the URL and content of a search result.
    """

    content_list = []
    driver = None
    try:
        # Initialize the Chrome WebDriver
        driver = init_driver()
        # Set the explicit wait time
        wait = WebDriverWait(driver, 30)
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
                # Extract URLs and content from search results
                contents = handle_search_results(search_results)
                content_list.extend(contents)
            except Exception as err:
                print(f"Extract google search output error for '{keyword}': {err}")
    except Exception as e:
        print(f"Init driver error: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Driver quit error: {str(e)}")
    return content_list
