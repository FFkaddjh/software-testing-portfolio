# 项目三：Selenium Web UI 自动化测试（Page Object 模式）

> 使用 Selenium WebDriver + pytest 对百度搜索进行 UI 自动化测试
> 对应简历中"项目二：百度搜索 UI 自动化练习"

---

## 项目结构

```
project_03_selenium_tests/
├── pages/                           # Page Object 层
│   ├── __init__.py
│   ├── base_page.py                 # 基类（封装的常用元素操作）
│   ├── baidu_home_page.py           # 百度首页 Page Object
│   └── baidu_search_results_page.py # 搜索结果页 Page Object
├── tests/                           # 测试用例
│   ├── conftest.py                  # 共享配置（WebDriver 创建、失败截图）
│   └── test_baidu_search.py         # 百度搜索测试（10+ 场景）
├── utils/                           # 工具模块
│   ├── __init__.py
│   ├── driver_factory.py            # WebDriver 工厂
│   └── screenshot.py                # 失败自动截图
├── screenshots/                     # 失败截图输出目录
├── pytest.ini                       # pytest 配置
├── requirements.txt                 # 依赖清单
└── README.md                        # 本文件
```

## 测试覆盖范围

| 测试类别 | 用例数 | 覆盖内容 |
|---------|--------|---------|
| 冒烟测试 | 2 | 首页加载、基本搜索 |
| 功能测试 | 8+ | 多关键词、搜索结果验证、点击跳转 |
| 边界测试 | 2+ | 空搜索、特殊字符搜索 |
| 国际化 | 2+ | 中文搜索、英文搜索 |
| **合计** | **14+** | |

## 使用方式

### 1. 安装依赖

```bash
cd project_03_selenium_tests
pip install -r requirements.txt
```

### 2. 安装浏览器驱动

```bash
# Chrome 浏览器需要安装 ChromeDriver（自动下载）
pip install webdriver-manager

# 或者手动下载 ChromeDriver: https://chromedriver.chromium.org/
# 放到系统 PATH 中
```

### 3. 运行测试

```bash
# 默认 Chrome 无头模式
pytest

# 有头模式（可以看到浏览器界面）
pytest --headless=false

# 使用 Firefox
pytest --browser=firefox

# 只跑冒烟测试
pytest -m smoke

# 生成带截图的 HTML 报告
pytest --html=report.html --self-contained-html
```

### 4. 运行单个测试文件

```bash
pytest tests/test_baidu_search.py -v
```

## 架构亮点

### Page Object 模式

```
tests/                  Page Objects（封装操作）      WebDriver（浏览器驱动）
    ↓                           ↓                           ↓
    测试用例  →→→→→→→→→→→→→→  BaiduHomePage  →→→→→→→→→→→  Chrome/Firefox
                             BaiduSearchResultsPage
```

- **Page Object**：每个页面用一个类封装，隐藏元素定位细节
- **基类封装**：`BasePage` 封装了 find / click / type / is_visible 等通用方法
- **链式调用**：`page.open().search("关键词")` 返回结果页对象
- **失败截图**：测试失败时自动截图保存到 screenshots/ 目录
- **参数化配置**：支持 --browser / --headless 命令行选项

## 简历写法

> ### 百度搜索 UI 自动化测试（Page Object 模式）
> - 使用 Selenium WebDriver + pytest 对百度搜索编写 14+ 条 UI 自动化测试用例
> - 采用 Page Object 设计模式，将页面元素和操作封装为独立类，提高脚本可维护性
> - 实现失败自动截图、参数化测试、跨浏览器支持（Chrome / Firefox）
> - 覆盖多关键词搜索、搜索结果验证、页面跳转、特殊字符等场景
> - 测试报告使用 pytest-html 生成，附带失败截图
> - 熟练掌握显式等待、隐式等待、元素定位策略（ID / CSS / XPath）
