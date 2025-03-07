import re
import time
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver


def setup_driver():
    """初始化 Selenium WebDriver"""

    # to avoid rejection by the website
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)


def search_ieee(title, human_mode=False):
    """在 IEEE Xplore 上搜索论文并返回第一个搜索结果的 URL。"""
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={urllib.parse.quote(title)}"
    print('title-based:', search_url)
    driver = setup_driver()
    try:
        driver.get(search_url)
        time.sleep(2)  # 等待加载
        result = driver.find_elements(By.CLASS_NAME, 'List-results-items')
        if result:
            link = result[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            print('paper-based:', link)
            return link
    finally:
        driver.quit()
    return None


def fetch_bibtex(ieee_url, human_mode=False):
    """获取论文的 BibTeX 信息。"""
    driver = setup_driver()
    try:
        driver.get(ieee_url)
        time.sleep(2)

        # 查找 "Cite This" 按钮并点击
        cite_button = driver.find_element(By.CLASS_NAME, 'xpl-btn-secondary')  # 使用正确的 class
        cite_button.click()
        time.sleep(1)

        # 切换到 BibTeX 选项卡（注意是 <a> 标签，而不是 <button>）
        bibtex_tab = driver.find_element(By.CSS_SELECTOR, 'a.document-tab-link[title="BibTeX"]')
        bibtex_tab.click()
        time.sleep(2)

        # 获取 BibTeX 文本 (正确的 class: `text ris-text`)
        bibtex_text = driver.find_element(By.CSS_SELECTOR, "pre.text.ris-text").text
        return bibtex_text
    finally:
        driver.quit()
    return None


if __name__ == '__main__':
    title = 'CALRA: Practical Conditional Anonymous and Leakage-Resilient Authentication Scheme for Vehicular Crowdsensing Communication'
    link = search_ieee(title, human_mode=True)
    if link:
        bibtex = fetch_bibtex(link, human_mode=True)
        print(bibtex)
