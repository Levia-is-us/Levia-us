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
    visual = os.getenv("VISUAL")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        if visual != "T":
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "plugins.plugins_disabled": ["Adobe Flash Player"],
        }
        if visual != "T":
            chrome_options.add_experimental_option("prefs", prefs)

        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        path = ChromeDriverManager().install()
        service = Service(path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(10)
        return driver

    except Exception as e:
        print(f"setup_driver WebDriver with error: {e}", file=sys.stderr)
        return None


def get_prompt_links(links, intent):
    links_json = json.dumps({"links": links, "intent": intent})

    result = create_chat_completion(
        system_prompt="You are a helpful assistant that filters links based on intent",
        model=CHAT_MODEL_NAME,
        prompt=get_links_filter_prompt(links_json),
        config={"temperature": 0, "max_tokens": 2000, "stream": False},
    )
    return json.loads(result)


def get_summary_links(links, intent):
    links_json = json.dumps({"links": links, "intent": intent})
    result = create_chat_completion(
        system_prompt="You are an AI assistant specialized in summarizing web pages. I will provide a list of multiple pages, each with a URL and its extracted text. Your task is to analyze the intent of each page and generate a comprehensive summary that combines and needs to be fully explained the key points from all pages based on their intent. The output should be in Markdown format.",
        model=CHAT_MODEL_NAME,
        prompt=links_summary_prompt.format(input=links_json),
        config={"temperature": 0.7, "stream": False},
    )

    return result


def get_Links(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    links = driver.find_elements(By.TAG_NAME, "a")
    domain = urlparse(url).scheme + "://" + urlparse(url).netloc
    path = urlparse(url).path
    link_data = [{"url": url, "text": "core page"}]

    for link in links:
        try:

            href = link.get_attribute("href")
            text = link.text

            if href:
                if is_absolute_url(href):
                    href = href
                else:
                    href = urljoin(domain, href)

                if path != urlparse(href).path:
                    link_data.append({"url": href, "text": text})

        except:
            continue

    return link_data


def get_all_links(urls):
    visual = os.getenv("VISUAL")
    links_data = []
    driver = setup_driver()

    for url in urls:
        links = get_Links(driver, url)
        links_data.extend(links)

    if visual == "T":
        smooth_scroll_to_bottom(driver)
    else:
        driver.quit()

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
    visual = os.getenv("VISUAL")
    results = []
    driver = setup_driver()
    for link in links:
        url = link["url"]
        driver.get(url)
        content = driver.find_element(By.TAG_NAME, "body").text
        link["content"] = content
        results.append(link)
        if visual == "T":
            smooth_scroll_to_bottom(driver)

    driver.quit()
    return results
