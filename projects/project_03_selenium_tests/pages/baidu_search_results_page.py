"""百度搜索结果页 — PageObject"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BaiduSearchResultsPage(BasePage):
    """搜索结果页的元素和操作"""

    # 元素定位器
    RESULT_ITEMS = (By.CSS_SELECTOR, "div.result")
    RESULT_LINKS = (By.CSS_SELECTOR, "div.result h3 a")
    SEARCH_INPUT = (By.ID, "kw")
    SEARCH_BUTTON = (By.ID, "su")
    PAGE_NAV = (By.CSS_SELECTOR, "div#page")
    RESULT_STATS = (By.CSS_SELECTOR, "div.opr-topnav1")

    def get_result_count(self) -> int:
        """获取当前页搜索结果的数量"""
        items = self.find_all(*self.RESULT_LINKS)
        return len(items)

    def get_result_titles(self) -> list:
        """获取所有搜索结果的标题文字"""
        links = self.find_all(*self.RESULT_LINKS)
        return [link.text for link in links if link.text.strip()]

    def get_result_urls(self) -> list:
        """获取所有搜索结果的链接"""
        links = self.find_all(*self.RESULT_LINKS)
        return [link.get_attribute("href") for link in links if link.get_attribute("href")]

    def click_result(self, index: int = 0):
        """点击第 N 个搜索结果"""
        links = self.find_all(*self.RESULT_LINKS)
        if index < len(links):
            links[index].click()
        else:
            raise IndexError(f"结果索引越界: {index}, 共 {len(links)} 个结果")

    def has_results(self) -> bool:
        """是否有搜索结果"""
        try:
            return len(self.find_all(*self.RESULT_LINKS, timeout=3)) > 0
        except:
            return False

    def search_again(self, keyword: str):
        """在结果页重新搜索"""
        self.type(*self.SEARCH_INPUT, keyword)
        self.click(*self.SEARCH_BUTTON)
        return BaiduSearchResultsPage(self.driver)
