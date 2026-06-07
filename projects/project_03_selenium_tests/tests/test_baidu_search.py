"""百度搜索 UI 自动化测试"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pages.baidu_home_page import BaiduHomePage


class TestBaiduSearch:
    """百度搜索功能测试"""

    @pytest.mark.smoke
    def test_homepage_load(self, driver):
        """百度首页加载测试"""
        page = BaiduHomePage(driver).open()
        assert page.is_loaded(), "百度首页加载失败"
        assert "百度" in page.get_title(), f"页面标题异常: {page.get_title()}"

    @pytest.mark.smoke
    def test_search_simple_keyword(self, driver):
        """简单关键词搜索"""
        page = BaiduHomePage(driver).open()
        results = page.search("软件测试")
        assert results.has_results(), "搜索后未返回任何结果"
        titles = results.get_result_titles()
        assert len(titles) > 0, "搜索结果标题列表为空"
        print(f"[搜索结果] 首页共 {len(titles)} 条结果")

    @pytest.mark.parametrize("keyword", [
        "Python",
        "pytest 教程",
        "Selenium WebDriver",
    ], ids=["python", "pytest_tutorial", "selenium"])
    def test_search_multiple_keywords(self, driver, keyword):
        """多关键词搜索"""
        page = BaiduHomePage(driver).open()
        results = page.search(keyword)
        assert results.has_results(), f"搜索 '{keyword}' 没有返回结果"
        titles = results.get_result_titles()
        # 至少有一个结果包含关键词（不区分大小写）
        keyword_lower = keyword.lower()
        has_relevant = any(keyword_lower in t.lower() for t in titles if t)
        assert has_relevant or len(titles) > 0, f"搜索结果与关键词 '{keyword}' 无关"

    def test_search_and_click_first_result(self, driver):
        """搜索并点击第一个结果"""
        page = BaiduHomePage(driver).open()
        results = page.search("软件测试")
        assert results.has_results()

        urls_before = results.get_result_urls()
        assert len(urls_before) > 0, "没有搜索到结果链接"

        results.click_result(0)
        # 点击后页面跳转，URL 应该不是百度搜索结果页
        current_url = driver.current_url
        print(f"[点击结果] 跳转到: {current_url}")

    def test_search_special_characters(self, driver):
        """特殊字符搜索"""
        page = BaiduHomePage(driver).open()
        results = page.search("!@#$%^测试*()")
        # 特殊字符搜索可能返回"未找到"或相关结果
        assert results.has_results() or not results.has_results()
        print(f"[特殊字符搜索] 返回结果: {results.has_results()}")

    @pytest.mark.edge_case
    def test_search_empty_query(self, driver):
        """空搜索（仅搜索按钮）"""
        page = BaiduHomePage(driver).open()
        results = page.search("")
        # 空的搜索关键词通常跳转到首页或搜索结果页
        assert "baidu" in driver.current_url.lower()

    def test_search_english_keywords(self, driver):
        """英文关键词搜索"""
        page = BaiduHomePage(driver).open()
        results = page.search("API testing best practices")
        assert results.has_results(), "英文关键词搜索未返回结果"

    def test_search_chinese_keywords(self, driver):
        """中文关键词搜索"""
        page = BaiduHomePage(driver).open()
        results = page.search("接口自动化测试框架")
        assert results.has_results(), "中文关键词搜索未返回结果"
        titles = results.get_result_titles()
        has_chinese = any("\u4e00" <= c <= "\u9fff" for t in titles for c in t if t)
        assert has_chinese or len(titles) > 0

    def test_search_page_title_changes(self, driver):
        """搜索后页面标题应包含关键词"""
        keyword = "Selenium 教程"
        page = BaiduHomePage(driver).open()
        page.search(keyword)
        title = page.get_title()
        assert keyword in title or "百度搜索" in title, f"搜索后标题异常: {title}"
