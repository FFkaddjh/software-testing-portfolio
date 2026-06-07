# 项目一：HTTPBin API 接口自动化测试

> 用 pytest + requests 对 [HTTPBin](https://httpbin.org) 进行全面的接口自动化测试
> 对应简历中"项目三：HTTPBin API 接口测试"

---

## 项目结构

`
project_01_httpbin_tests/
├── conftest.py                 # 共享配置（Session、URL、测试数据）
├── test_httpbin_basic.py       # 核心 HTTP 方法（GET/POST/PUT/PATCH/DELETE）
├── test_httpbin_auth.py        # 认证 + HTTP 状态码覆盖（30+种）
├── test_httpbin_data_formats.py# 数据格式（JSON/Form/File/Cookie/编码）
├── test_httpbin_dynamic.py     # 动态响应（延迟/流式/IP/重定向）
├── pytest.ini                  # pytest 配置
├── requirements.txt            # 依赖清单
└── README.md                   # 本文件
`

## 测试覆盖范围

| 测试类别 | 文件 | 用例数 | 覆盖内容 |
|---------|------|--------|---------|
| 基础方法 | test_httpbin_basic.py | 10+ | GET/POST/PUT/PATCH/DELETE + 参数/Header |
| 认证安全 | test_httpbin_auth.py | 40+ | Basic Auth / Bearer / Digest / 30+ 状态码 / 重定向 |
| 数据格式 | test_httpbin_data_formats.py | 10+ | JSON / Form / 文件上传 / Cookie / 大数据量 |
| 动态场景 | test_httpbin_dynamic.py | 12+ | 延迟响应 / 流式 / IP / UUID / 缓存 / ETag |
| **合计** | | **70+** | |

## 使用方式

### 1. 安装依赖

`ash
cd project_01_httpbin_tests
pip install -r requirements.txt
`

### 2. 运行全部测试

`ash
pytest
`

### 3. 按标签运行

`ash
pytest -m smoke          # 只跑冒烟测试
pytest -m auth           # 只跑认证测试
pytest -m edge_case      # 只跑边界场景
pytest -m \"not slow\"    # 跳过慢速测试
`

### 4. 生成测试报告

`ash
pytest --html=report.html --self-contained-html
`

### 5. 使用 pytest-reportlog（正好用上克隆的项目）

`ash
pip install pytest-reportlog
pytest --report-log=result.jsonl
`

## 依赖

- Python 3.9+
- pytest >= 7.0
- requests >= 2.28
- （可选）pytest-html 生成可视化报告
- （可选）pytest-reportlog 生成 JSON 行日志

## 简历写法

将此项目写入简历时，可以参考：

> ### HTTPBin API 接口自动化测试
> - 使用 pytest + requests 对 HTTPBin 公开 API 编写 70+ 条自动化测试用例
> - 覆盖 GET/POST/PUT/PATCH/DELETE 五种核心方法及 30+ 种 HTTP 状态码
> - 实现 Basic Auth / Bearer Token / Digest Auth 等认证场景的自动化验证
> - 测试数据格式：JSON、Form、文件上传、Cookie、大数据量 payload
> - 使用 pytest 插件机制生成 HTML 测试报告和 JSON 行日志
