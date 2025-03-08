import re
import time
import requests
import urllib.parse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import random


def setup_driver():
    """Initializes a new Selenium WebDriver instance.

    Returns:
        WebDriver: A new instance of Selenium WebDriver.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # this is tested on macOS
    if platform.system() == 'Darwin':
        service = Service()
    else:
        service = webdriver.ChromeService()
        # service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=chrome_options)


def human_delay(min_delay=1, max_delay=3):
    """Simulate human-like delays."""
    time.sleep(random.uniform(min_delay, max_delay))


def search_ieee(title):
    """Searches IEEE Xplore for a paper by title and returns the URL of the first result.

    Args:
        title (str): The title of the paper to search for.

    Returns:
        str: The URL of the first search result, or None if no result is found.
    """
    # Construct the search URL
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={urllib.parse.quote(title)}"
    os.write(1, f"title-based: {search_url}\n".encode())
    driver = setup_driver()
    try:
        driver.get(search_url)
        human_delay(3, 5)
        os.write(1, f"{driver.page_source}\n".encode())
        result = driver.find_elements(By.CLASS_NAME, 'List-results-items')
        if result:
            link = result[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            os.write(1, f"paper-based: {link}\n".encode())
            return link
    finally:
        driver.quit()
    return None


def dismiss_cookie_banner(driver):
    try:
        # Wait briefly for the cookie consent banner to appear
        banner = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'][aria-label*='Cookie']"))
        )
        # Attempt to click the accept button within the banner, if present
        accept_button = banner.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", accept_button)
        human_delay(1, 2)
    except Exception:
        pass  # If not found, continue


def fetch_bibtex(ieee_url):
    """Fetches the BibTeX information of a paper from its IEEE Xplore URL.

    Args:
        ieee_url (str): The URL of the paper on IEEE Xplore.

    Returns:
        str: The BibTeX entry of the paper, or None if not found.
    """
    driver = setup_driver()
    try:
        driver.get(ieee_url)
        human_delay(1, 2)
        # Dismiss cookie consent banner if present
        dismiss_cookie_banner(driver)
        # Find and click the "Cite This" button
        cite_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'xpl-btn-secondary'))
        )
        driver.execute_script("arguments[0].click();", cite_button)
        human_delay(2, 3)
        # Switch to the BibTeX tab
        bibtex_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.document-tab-link[title="BibTeX"]'))
        )
        driver.execute_script("arguments[0].click();", bibtex_tab)
        human_delay(2, 3)
        # Get the BibTeX text
        bibtex_text = driver.find_element(By.CSS_SELECTOR, "pre.text.ris-text").text
        os.write(1, f"bibtex: {bibtex_text}\n".encode())
        return bibtex_text
    finally:
        driver.quit()
    return None


if __name__ == '__main__':
    title = 'CALRA: Practical Conditional Anonymous and Leakage-Resilient Authentication Scheme for Vehicular Crowdsensing Communication'
    link = search_ieee(title)
    if link:
        bibtex = fetch_bibtex(link)
        os.write(1, f"{bibtex}\n".encode())
