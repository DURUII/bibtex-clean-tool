import re
import time
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.core.os_manager import ChromeType
import streamlit as st
import os  # new import
import platform  # new import

# New: cache the driver resource to avoid reinitializing for every call


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Use platform to determine environment (macOS vs. cloud)
    if platform.system() == "Darwin":
        service = Service()
    else:
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    return webdriver.Chrome(service=service, options=chrome_options)


def setup_driver():
    """Initializes (or retrieves) Selenium WebDriver using cached resource.

    Returns:
        WebDriver: A cached instance of Selenium WebDriver.
    """
    return get_driver()


def search_ieee(title, human_mode=False):
    """Searches IEEE Xplore for a paper by title and returns the URL of the first result.

    Args:
        title (str): The title of the paper to search for.
        human_mode (bool, optional): If True, enables human interaction mode. Defaults to False.

    Returns:
        str: The URL of the first search result, or None if no result is found.
    """
    # Construct the search URL
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={urllib.parse.quote(title)}"
    print('title-based:', search_url)
    driver = setup_driver()
    try:
        driver.get(search_url)
        time.sleep(2)  # Wait for the page to load
        result = driver.find_elements(By.CLASS_NAME, 'List-results-items')
        if result:
            link = result[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            print('paper-based:', link)
            return link
    finally:
        # If you wish to quit the driver after each operation, you may call driver.quit()
        # However, with a cached resource, it is generally better to reuse the session.
        driver.quit()
    return None


def fetch_bibtex(ieee_url, human_mode=False):
    """Fetches the BibTeX information of a paper from its IEEE Xplore URL.

    Args:
        ieee_url (str): The URL of the paper on IEEE Xplore.
        human_mode (bool, optional): If True, enables human interaction mode. Defaults to False.

    Returns:
        str: The BibTeX entry of the paper, or None if not found.
    """
    driver = setup_driver()
    try:
        driver.get(ieee_url)
        time.sleep(2)

        # Find and click the "Cite This" button
        cite_button = driver.find_element(By.CLASS_NAME, 'xpl-btn-secondary')
        cite_button.click()
        time.sleep(1)

        # Switch to the BibTeX tab
        bibtex_tab = driver.find_element(By.CSS_SELECTOR, 'a.document-tab-link[title="BibTeX"]')
        bibtex_tab.click()
        time.sleep(2)

        # Get the BibTeX text
        bibtex_text = driver.find_element(By.CSS_SELECTOR, "pre.text.ris-text").text
        return bibtex_text
    finally:
        driver.quit()  # Decide if you want to close the driver or keep it cached.
    return None


if __name__ == '__main__':
    title = 'CALRA: Practical Conditional Anonymous and Leakage-Resilient Authentication Scheme for Vehicular Crowdsensing Communication'
    link = search_ieee(title, human_mode=True)
    if link:
        bibtex = fetch_bibtex(link, human_mode=True)
        print(bibtex)
