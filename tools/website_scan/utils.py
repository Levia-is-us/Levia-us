import sys
from urllib.parse import urljoin, urlparse
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
from tools.website_scan.links_filter_prompt import links_filter_prompt
from tools.website_scan.links_summary_prompt import links_summary_prompt
from tools.website_scan.chat_gpt import chat_gpt
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)


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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "plugins.plugins_disabled": ["Adobe Flash Player"],
        }
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
    prompt = [
        {"role": "assistant", "content": links_filter_prompt},
        {"role": "user", "content": f"{links_json}"},
    ]

    result = chat_gpt(prompt, config={"temperature": 0.7})
    return json.loads(result)


def get_summary_links(links, intent):
    links_json = json.dumps({"links": links, "intent": intent})
    prompt = [
        {"role": "assistant", "content": links_summary_prompt},
        {"role": "user", "content": f"{links_json}"},
    ]

    result = chat_gpt(prompt, config={"temperature": 0.7})

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
    links_data = []
    driver = setup_driver()

    for url in urls:
        links = get_Links(driver, url)
        links_data.extend(links)

    driver.quit()
    return links_data


def get_all_content(links):
    results = []
    driver = setup_driver()
    for link in links:
        url = link["url"]
        driver.get(url)
        content = driver.find_element(By.TAG_NAME, "body").text
        link["content"] = content
        results.append(link)

    driver.quit()
    return results
