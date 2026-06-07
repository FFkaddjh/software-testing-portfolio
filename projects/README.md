# 🚀 开源项目实战记录

## 已完成的第一个项目：pytest-reportlog

### 项目简介
pytest 官方插件，将测试结果以 JSON 格式输出到日志文件，方便机器解析。

### Issue 信息
- **Issue #83**: "remove ANSI escape sequences from the report messages"
- **地址**: https://github.com/pytest-dev/pytest-reportlog/issues/83
- **问题描述**: pytest 在错误 diff 中添加了 ANSI 彩色转义序列，导致 reportlog 日志文件中出现不可读的垃圾字符。由于日志文件是给机器解析的，这些转义字符应该被清除。

### 我的修改

#### 1. `src/pytest_reportlog/plugin.py`（核心修改）

**添加了 ANSI 转义序列的正则表达式：**
```python
_ansi_re = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
```
这个正则覆盖了所有常见 ANSI 序列，包括：
- 基本颜色: `\x1b[31m`
- 256色模式: `\x1b[38;5;196m`
- 私有序列: `\x1b[?25l`
- 复合序列: `\x1b[92;103m`

**添加了递归清理函数 `_strip_ansi_from_data()`：**
- 递归遍历 dict / list / tuple / 字符串
- 只清理字符串值，int、None 等类型原样保留
- 保留原始数据结构

**在 `_write_json_data()` 中调用清理：**
- JSON 序列化之前先清理数据
- 对异常类型（`TypeError/ValueError`）也做清理

#### 2. `tests/test_ansi_stripping.py`（测试文件，7 个测试用例）

| 测试函数 | 测试内容 |
|---|---|
| `test_strip_ansi_from_data` | 参数化测试：简单字符串、dict、嵌套dict、list、混合类型 |
| `test_ansi_stripping_does_not_affect_normal_data` | 没有 ANSI 的数据不应被改动 |
| `test_ansi_stripping_preserves_data_structure` | 数据结构（如 tuple 中的 tuple）不被破坏 |
| `test_complex_ansi_sequences` | 10 种不同的 ANSI 序列模式 |
| `test_integration_with_report_log` | 集成测试：实际跑 pytest 后验证日志是干净的 JSON |
| `test_cleanup_unserializable_with_ansi` | 同时处理不可序列化数据和 ANSI 转义 |

### Git 状态
- 分支: `fix-remove-ansi-escape-sequences`
- 修改: `plugin.py` (28 行新增, 8 行删除)
- 新增: `tests/test_ansi_stripping.py`

---

## 📂 项目文件夹结构

```
D:\my_resume_project\
├── materials\
│   ├── resume.md              ← 原始简历
│   └── target_jd.txt
├── output\
│   ├── README.md              ← 总索引
│   ├── resume_polished.md     ← 润色后的简历
│   ├── learning_roadmap.md    ← 学习路线
│   ├── opensource_projects.md ← 开源项目推荐
│   └── projects\
│       └── pytest-reportlog\  ← 已克隆到本地的项目
│           ├── src\pytest_reportlog\plugin.py (已修改)
│           └── tests\test_ansi_stripping.py (新增)
```

---

## 🎯 推荐参与顺序

### 第一步（当前已完成）
✅ **pytest-reportlog** — 清理 ANSI 转义序列
- 代码量小，问题明确
- 已克隆到本地并完成修改

### 第二步：提交 PR（需要你注册 GitHub 账号）
1. 去 https://github.com/join 注册 GitHub 账号
2. Fork https://github.com/pytest-dev/pytest-reportlog
3. 在本地把远端的 origin 改成你的 fork
4. 提交 commit 并 push
5. 在 GitHub 上创建 Pull Request

### 第三步：继续参与
按难度排序的后续项目：

| 项目 | Stars | 难度 | 当前可用 Issue |
|---|---|---|---|
| https://github.com/pytest-dev/pytest-messenger | - | ⭐ 最简单 | Issue #166 (显示重跑信息), #137 (Telegram 支持), #136 (Discord 支持) |
| https://github.com/pytest-dev/pytest-bdd | 1451 | ⭐⭐ | Issue #535 (场景生成), #476 (打印标签) |
| https://github.com/pytest-dev/pytest-nunit | - | ⭐⭐ | Issue #35 (序列化运行设置) |
| https://github.com/buildbot/buildbot | 5448 | ⭐⭐⭐ | 7 个 good first issue |
| https://github.com/httprunner/hrp | 84 | ⭐⭐ | HTTP(S) 测试工具，中文友好 |

### 个人练习题（不需要注册即可开始）
1. **JSONPlaceholder** — 用 pytest + requests 写 API 自动化测试
2. **Sauce Demo** — 用 Selenium 写 UI 自动化测试
3. **HTTPBin** — 练习接口测试的各种场景

---

## ⚠️ 如何运行测试
当前机器没有安装 Python。回到你的电脑后：
```bash
# 安装 Python 3.11+（如果还没装）
# 然后：
cd D:\my_resume_project\output\projects\pytest-reportlog
pip install -e ".[dev]"
pytest tests/ -v
```

---

## 💡 对我简历的好处
把 "pytest-reportlog" 的 PR 链接放到简历里，效果远大于"了解 pytest"。面试官看到真实开源项目的贡献记录，对你的印象会完全不同。
