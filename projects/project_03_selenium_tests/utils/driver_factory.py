"""WebDriver 工厂 — 支持 Chrome 和 Firefox，自动管理驱动"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def create_driver(browser: str = "chrome", headless: bool = True):
    """创建 WebDriver 实例，自动下载/匹配驱动"""
    browser = browser.lower()

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--lang=zh-CN")
        # 禁用自动化提示和弹窗
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = ChromeService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"不支持的浏览器: {browser}")

    driver.implicitly_wait(5)
    driver.set_page_load_timeout(30)
    return driver