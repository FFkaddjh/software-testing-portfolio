# 项目二：Flask TODO 应用功能测试

> 搭建一个完整的 Flask TODO Web 应用作为测试目标，编写全面的功能测试用例
> 对应简历中"项目一：Todo List Web 应用功能测试"

---

## 项目结构

```
project_02_flask_todo_tests/
├── app/                          # TODO 应用（测试目标）
│   ├── app.py                    # Flask 应用（7 个 RESTful API 端点）
│   └── templates/
│       └── index.html            # 前端页面
├── tests/                        # 测试套件
│   ├── conftest.py               # 共享夹具
│   ├── test_todo_api.py          # 创建/查询功能测试
│   ├── test_todo_crud.py         # 更新/删除/切换/清除测试
│   └── test_todo_edge_cases.py   # 边界场景测试（30+ 场景）
├── pytest.ini                    # pytest 配置
├── requirements.txt              # 依赖清单
└── README.md                     # 本文件
```

## 测试覆盖范围

| 测试类别 | 文件 | 用例数 | 覆盖内容 |
|---------|------|--------|---------|
| 创建功能 | test_todo_api.py | 7+ | 正常创建、空标题、空格、无请求体、超长标题 |
| 查询功能 | test_todo_api.py | 5+ | 获取全部、按 ID 查询、空列表、404 处理 |
| 更新功能 | test_todo_crud.py | 7+ | 更新标题、状态、同时更新、无效状态 |
| 删除功能 | test_todo_crud.py | 4+ | 正常删除、数量验证、404 处理 |
| 状态切换 | test_todo_crud.py | 4+ | pending→completed→pending |
| 清除已完成 | test_todo_crud.py | 3+ | 清除全部、数量为 0 |
| 边界场景 | test_todo_edge_cases.py | 12+ | 连续操作、特殊字符、过滤、并发 |
| **合计** | | **40+** | |

## 使用方式

### 1. 启动 TODO 应用

```bash
cd app
pip install flask
python app.py
# 访问 http://localhost:5000
```

### 2. 运行测试

```bash
cd project_02_flask_todo_tests
pip install -r requirements.txt
pytest
```

### 3. 生成测试报告

```bash
pytest --html=report.html --self-contained-html
```

### 4. 按标签运行

```bash
pytest -m smoke       # 冒烟测试
pytest -m edge_case   # 边界场景
```

## 测试用例设计方法（面试可用）

本项目展示了以下测试设计方法的应用：

| 方法 | 应用场景 | 示例 |
|------|---------|------|
| **等价类划分** | 标题长度 | 有效：1-200 字符；无效：0 字符、>200 字符 |
| **边界值分析** | 标题长度边界 | 0、1、200、201 字符 |
| **异常场景** | 各种异常输入 | 空请求体、无效状态值、不存在的 ID |
| **状态转换** | TODO 状态流转 | pending → completed → pending |
| **场景法** | 连续操作流 | 创建 → 更新 → 切换 → 删除 |
| **参数化测试** | 多种数据组合 | 不同标题类型、不同请求参数 |

## 简历写法

> ### Todo List Web 应用功能测试
> - 使用 Flask 搭建 TODO Web 应用，包含 7 个 RESTful API 端点
> - 基于 pytest 编写 40+ 条自动化测试用例，覆盖创建、查询、更新、删除全流程
> - 应用等价类划分、边界值分析等黑盒测试方法设计测试数据
> - 实现状态切换、批量清除、状态过滤等业务场景的自动化验证
> - 使用 pytest-html 生成可视化测试报告
