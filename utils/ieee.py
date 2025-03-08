import re
import time
import requests
import urllib.parse
import os
import random
import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


def setup_driver():
    """
    Initialize and return a configured Selenium Chrome WebDriver.

    - Configured to run in headless mode.
    - Sets a realistic user-agent.
    - Disables GPU, sandboxing, and other automation-detectable features.
    """
    local = False
    if platform.system() == 'Darwin':
        local = True

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in headless mode for automation
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Set user-agent to mimic a real browser session
    if not local:
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    # Exclude automation switches to reduce detection risk
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Initialize Service based on platform; using default for macOS, other platforms get default Service
    if local:
        service = Service()
    else:
        service = webdriver.ChromeService()
        # Alternatively, uncomment below to use webdriver_manager for installation
        # service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=chrome_options)


def human_delay(min_delay=1, max_delay=3):
    """
    Pause execution for a random interval between min_delay and max_delay seconds.
    This simulates human-like delays to reduce automated detection.
    """
    time.sleep(random.uniform(min_delay, max_delay))


def search_ieee(title):
    """
    Search IEEE Xplore for a paper by its title.

    Constructs a search URL using the provided title, loads the page,
    and extracts the URL of the first result.

    Args:
        title (str): Title of the target paper.

    Returns:
        str: URL of the first search result, or None if not found.
    """
    # Encode title into URL and build search URL
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={urllib.parse.quote(title)}"
    os.write(1, f"title-based: {search_url}\n".encode())

    driver = setup_driver()
    try:
        driver.get(search_url)
        human_delay(3, 5)  # Allow page to load and dynamic elements to render
        # Output page source for debugging purposes
        os.write(1, f"{driver.page_source}\n".encode())
        # Find elements containing search results; class name may need updating if IEEE changes their layout
        result = driver.find_elements(By.CLASS_NAME, 'List-results-items')
        if result:
            # Extract the first result's link from its anchor tag
            link = result[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            os.write(1, f"paper-based: {link}\n".encode())
            return link
    finally:
        driver.quit()  # Ensure driver is closed even if an error occurs
    return None


def dismiss_cookie_banner(driver):
    """
    Look for and dismiss the cookie consent banner if present.

    Uses an explicit wait to detect the banner and clicks the accept button.

    Args:
        driver (WebDriver): The active Selenium WebDriver instance.
    """
    try:
        # Wait up to 5 seconds for the cookie consent banner to appear
        banner = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'][aria-label*='Cookie']"))
        )
        # Find the button inside the banner and click it using JavaScript to avoid click interception issues
        accept_button = banner.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", accept_button)
        human_delay(1, 2)  # Short delay to allow the banner to disappear
    except Exception:
        # If banner not found or any error occurs, continue without interruption
        pass


def fetch_bibtex(ieee_url):
    """
    Fetch the BibTeX entry from an IEEE Xplore paper page.

    Navigates to the paper's page, dismisses cookie banners, clicks the "Cite This" button,
    switches to the BibTeX tab, and retrieves the BibTeX text.

    Args:
        ieee_url (str): URL of the IEEE paper.

    Returns:
        str: The BibTeX entry as text, or None if retrieval fails.
    """
    driver = setup_driver()
    try:
        driver.get(ieee_url)
        human_delay(1, 2)  # Allow page to start rendering

        # Dismiss cookie consent banner if it appears
        dismiss_cookie_banner(driver)

        # Wait until the "Cite This" button is clickable, then click it using JavaScript
        cite_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'xpl-btn-secondary'))
        )
        driver.execute_script("arguments[0].click();", cite_button)
        human_delay(2, 3)

        # Wait until the BibTeX tab is clickable, then click it
        bibtex_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.document-tab-link[title="BibTeX"]'))
        )
        driver.execute_script("arguments[0].click();", bibtex_tab)
        human_delay(2, 3)

        # Retrieve the BibTeX text from the designated preformatted text element
        bibtex_text = driver.find_element(By.CSS_SELECTOR, "pre.text.ris-text").text
        os.write(1, f"bibtex: {bibtex_text}\n".encode())
        return bibtex_text
    finally:
        driver.quit()  # Always close the driver to free resources
    return None


if __name__ == '__main__':
    # Define the paper title to search for
    title = 'CALRA: Practical Conditional Anonymous and Leakage-Resilient Authentication Scheme for Vehicular Crowdsensing Communication'
    # Search for the paper and obtain the URL
    link = search_ieee(title)
    if link:
        # Fetch and output the BibTeX entry from the paper page
        bibtex = fetch_bibtex(link)
        os.write(1, f"{bibtex}\n".encode())
