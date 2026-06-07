"""百度搜索首页 — PageObject"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class BaiduHomePage(BasePage):
    """百度首页的元素和操作"""

    # 元素定位器
    SEARCH_INPUT = (By.ID, "kw")
    SEARCH_BUTTON = (By.ID, "su")

    def open(self):
        """打开百度首页并关闭可能弹窗"""
        self.driver.get("https://www.baidu.com")
        # 尝试关闭可能出现的弹窗/覆盖层
        import time
        time.sleep(1)
        try:
            # 常见的弹窗关闭按钮
            for selector in [".s_ipt_wr", "#kw"]:
                el = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if el:
                    break
        except Exception:
            pass
        return self

    def search(self, keyword: str):
        """输入搜索关键词并点击搜索"""
        self.type(*self.SEARCH_INPUT, keyword)
        self.click(*self.SEARCH_BUTTON)
        from pages.baidu_search_results_page import BaiduSearchResultsPage
        return BaiduSearchResultsPage(self.driver)

    def is_loaded(self) -> bool:
        """检查百度首页是否加载完成"""
        try:
            el = self.find(*self.SEARCH_INPUT, timeout=5)
            return el.is_displayed()
        except Exception:
            return False

    def get_search_input_placeholder(self) -> str:
        """获取搜索框的 placeholder 文本"""
        element = self.find(*self.SEARCH_INPUT)
        return element.get_attribute("placeholder") or ""
