# 百度搜索 UI 自动化测试

## 这个项目是干嘛的

用 Selenium + Page Object 模式写百度搜索的自动化测试。一共11条，全部通过。

## 框架结构

```
pages/
  base_page.py              # 基类，封装的常用操作
  baidu_home_page.py        # 百度首页
  baidu_search_results_page.py  # 搜索结果页
tests/
  test_baidu_search.py      # 测试用例
utils/
  driver_factory.py         # WebDriver 工厂
  screenshot.py             # 失败截图
```

## 测试内容

- 首页加载验证
- 各种关键词搜索（中文、英文、特殊字符）
- 搜索结果验证
- 点击结果跳转

## 遇到的问题

百度会检测自动化浏览器，弹安全验证页面。搞了好几种方法才绕过：
1. 禁用自动化标志
2. 覆盖 navigator.webdriver 属性
3. 设置合理的 User-Agent
4. 在页面注入脚本来绕过检测

## 怎么跑

```bash
cd project_03_selenium_tests
pip install -r requirements.txt
python -m pytest -v
```

想看到浏览器界面的话：
```bash
python -m pytest -v --headless false
```

## 结果

11/11 通过。

## 学到的东西

- Page Object 模式让 UI 测试好维护多了
- 失败截图对定位问题帮助很大
- webdriver-manager 自动管驱动版本，省事
- 国内网站基本都有反爬，做自动化要留个心眼
