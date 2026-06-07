"""失败截图工具"""
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver


SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


def take_screenshot(driver: WebDriver, test_name: str):
    """在测试失败时截图保存"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"[截图已保存] {filepath}")
    return filepath
