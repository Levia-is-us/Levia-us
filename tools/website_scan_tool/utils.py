import sys
import time
from urllib.parse import urljoin, urlparse
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
from engine.llm_provider.llm import create_chat_completion
from tools.website_scan_tool.links_filter_prompt import get_links_filter_prompt
from tools.website_scan_tool.links_summary_prompt import links_summary_prompt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME")
visual = os.getenv("VISUAL")

def remove_duplicate_links(links):
    seen_urls = set()
    unique_links = []

    for link in links:
        url = link["url"]
        if not url.startswith(("http://", "https://")):
            continue

        if url not in seen_urls:
            seen_urls.add(url)
            unique_links.append(link)

    return unique_links


def is_absolute_url(url):
    return bool(urlparse(url).netloc)


def setup_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        if visual != "True":
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "plugins.plugins_disabled": ["Adobe Flash Player"],
        }
        if visual != "True":
            chrome_options.add_experimental_option("prefs", prefs)

        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if visual == "True":
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
            )
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
        path = ChromeDriverManager().install()
        service = Service(path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(60)
        return driver

    except Exception as e:
        print(f"setup_driver WebDriver with error: {e}", file=sys.stderr)
        return None


def get_prompt_links(links, intent):
    try:
        links_json = json.dumps({"links": links, "intent": intent})

        result = create_chat_completion(
            system_prompt="You are a helpful assistant that filters links based on intent",
            model=CHAT_MODEL_NAME,
            prompt=get_links_filter_prompt(links_json),
            config={"temperature": 0, "max_tokens": 2000, "stream": False},
        )
    except Exception as e:
        raise Exception(e)

    return json.loads(result)


def get_summary_links(links, intent):
    links_json = json.dumps({"links": links, "intent": intent, "time": time.strftime("%Y/%m/%d")})
    try:
        result = create_chat_completion(
        system_prompt="You are an AI assistant specialized in summarizing web pages. I will provide a list of multiple pages, each with a URL and its extracted text. Your task is to analyze the intent of each page and generate a comprehensive summary that combines and needs to be fully explained the key points from all pages based on their intent. The output should be in Markdown format.",
        model=CHAT_MODEL_NAME,
        prompt=links_summary_prompt.format(input=links_json),
        config={"temperature": 0.7, "stream": False},
    )

    except Exception as e:
        raise Exception(e)
    return result

def get_Links(url):
    link_data = [{"url": url, "text": "core page"}]

    return link_data


def get_all_links(urls):
    links_data = []

    for url in urls:
        links = get_Links(url)
        links_data.extend(links)

    return links_data


def smooth_scroll_to_bottom(driver, duration=2.0):
    total_height = driver.execute_script("return document.body.scrollHeight")

    step_time = 0.01
    steps = int(duration / step_time)

    step_height = total_height / steps

    current_height = 0

    start_time = time.time()
    for i in range(steps):
        current_height += step_height
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(step_time)

        if time.time() - start_time > duration:
            break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def get_all_content(links):
    if(len(links) == 0):
       raise Exception("No links found")

    visual = os.getenv("VISUAL")
    results = []
    driver = setup_driver()
    error = ''
    for link in links:
        try:
            url = link["url"]
            driver.get(url)
            content = driver.find_element(By.TAG_NAME, "body").text
            link["content"] = content
            results.append(link)
            if visual == "True":
                smooth_scroll_to_bottom(driver)
        except Exception as e:
            error = e
            pass

    driver.quit()
    if(len(results) == 0):
       raise Exception(error)
    return results
