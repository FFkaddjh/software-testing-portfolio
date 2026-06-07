"""Page Object 基类 — 封装常用元素操作"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """所有 Page Object 的基类"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find(self, by: By, value: str, timeout: int = 10):
        """查找单个元素（带显式等待）"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_all(self, by: By, value: str, timeout: int = 10):
        """查找所有匹配元素（带显式等待）"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return self.driver.find_elements(by, value)

    def click(self, by: By, value: str, timeout: int = 10):
        """点击元素（带可点击等待）"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()

    def type(self, by: By, value: str, text: str, timeout: int = 10):
        """输入文本（优先用 JS，绕过弹窗遮挡）"""
        element = self.find(by, value, timeout)
        # 用 JS 设置值，绕过弹窗遮挡
        self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
        # 触发 input 事件（对需要 JS 事件的页面有效）
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", element)

    def get_text(self, by: By, value: str, timeout: int = 10) -> str:
        """获取元素文本"""
        return self.find(by, value, timeout).text

    def is_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """判断元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except:
            return False

    def get_title(self) -> str:
        """获取页面标题"""
        return self.driver.title

    def get_current_url(self) -> str:
        """获取当前 URL"""
        return self.driver.current_url
