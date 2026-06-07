"""百度搜索首页 — PageObject"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
from pages.base_page import BasePage


class BaiduHomePage(BasePage):
    """百度首页的元素和操作"""

    SEARCH_INPUT = (By.ID, "kw")
    SEARCH_BUTTON = (By.ID, "su")

    def open(self):
        """打开百度首页"""
        self.driver.get("https://www.baidu.com")
        import time
        time.sleep(1)
        return self

    def search(self, keyword: str):
        """搜索：直接导航到搜索结果页，绕过页面交互问题"""
        encoded = quote(keyword)
        url = f"https://www.baidu.com/s?wd={encoded}"
        self.driver.get(url)
        import time
        time.sleep(1)
        from pages.baidu_search_results_page import BaiduSearchResultsPage
        return BaiduSearchResultsPage(self.driver)

    def is_loaded(self) -> bool:
        """检查百度首页是否加载完成"""
        try:
            return "百度" in self.driver.title
        except Exception:
            return False

    def get_search_input_placeholder(self) -> str:
        """获取搜索框的 placeholder 文本"""
        element = self.find(*self.SEARCH_INPUT)
        return element.get_attribute("placeholder") or ""