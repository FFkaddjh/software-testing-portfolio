"""Selenium 测试共享配置与夹具"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.driver_factory import create_driver
from utils.screenshot import take_screenshot


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="浏览器类型: chrome / firefox")
    parser.addoption("--headless", action="store", default="true",
                     choices=["true", "false"], help="无头模式: true/false")


@pytest.fixture(scope="function")
def driver(request):
    """为每个测试创建 WebDriver 实例，测试结束后自动退出"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") == "true"
    _driver = create_driver(browser, headless)
    yield _driver
    _driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            take_screenshot(driver, item.nodeid.replace("::", "_").replace("/", "_"))
