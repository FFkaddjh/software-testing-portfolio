# 软件测试求职资料汇总

> 为 胡鑫绵 定制
> 生成日期：2026年6月7日

---

## 文件目录

| 文件 | 说明 |
|------|------|
| [resume_polished.md](./resume_polished.md) | 润色后的简历，直接可用于求职投递 |
| [learning_roadmap.md](./learning_roadmap.md) | 零基础转软件测试的学习路线（5个阶段 + 时间表） |
| [opensource_projects.md](./opensource_projects.md) | 开源项目推荐 + 练习平台 + 行动计划 |

## 实战项目代码（简历中三个项目的完整实现）

| 项目 | 目录 | 代码量 | 覆盖内容 | 技术栈 |
|------|------|--------|---------|--------|
| 🥇 HTTPBin API 接口自动化测试 | [projects/project_01_httpbin_tests/](./projects/project_01_httpbin_tests/) | 70+ 用例 | 5种HTTP方法、30+状态码、认证、Cookie、重定向、延迟响应 | pytest + requests |
| 🥇 Flask TODO 应用功能测试 | [projects/project_02_flask_todo_tests/](./projects/project_02_flask_todo_tests/) | 40+ 用例 | 创建/查询/更新/删除/切换/清除、边界场景、状态过滤 | Flask + pytest |
| 🥇 Selenium UI 自动化测试 | [projects/project_03_selenium_tests/](./projects/project_03_selenium_tests/) | 14+ 用例 | 页面加载、多关键词搜索、结果验证、Page Object 模式 | Selenium + pytest |

> 三个项目合计 **120+ 条自动化测试用例**，覆盖接口、Web UI、功能测试三大方向

---

## 已克隆的开源项目

| 项目 | 目录 | 说明 |
|------|------|------|
| pytest-reportlog | [projects/pytest-reportlog/](./projects/pytest-reportlog/) | pytest 报告日志插件，已含测试用例，可研究贡献方向 |

---

## 快速开始

### 如果你是第一次接触测试

1. **先看学习路线** → [learning_roadmap.md](./learning_roadmap.md)，了解全局
2. **从最简单的项目开始** → 打开项目一 [HTTPBin 测试](./projects/project_01_httpbin_tests/)，看看测试用例怎么写
3. **本地跑起来试试** → 安装 Python 3.11+，进入项目目录，`pip install -r requirements.txt && pytest`
4. **把练习记下来** → 把跑通过的测试用例写到简历里

### 如果已经有一些基础

1. 直接跑三个项目的测试，看看真实的测试代码长什么样
2. 研究 [pytest-reportlog](./projects/pytest-reportlog/) 的源码和 Issue，尝试贡献
3. 把项目三的 Selenium 测试改成其他网站（如 Sauce Demo）

---

## 给你的三点建议

1. **面试时活用物理学背景** — 控制变量法 = 测试方法论，物理实验报告 = 测试报告，分析数据找异常值 = 找 Bug。这些类比面试官会很有共鸣。
2. **不要等"学完了再投"** — 学完前两个阶段就可以开始投简历，边面试边补漏，面试经验本身也是学习。
3. **GitHub 就是你的工作经验** — 把这三个项目的代码推到 GitHub 上，面试时给人看，比空口说"我会"有力一百倍。

---

## 下一步做什么？

- 把三个项目 Push 到你的 GitHub
- 跑通所有测试（安装 Python 后：`pip install -r 每个项目的 requirements.txt`）
- 把 Selenium 测试扩展到其他练习网站（Sauce Demo、OrangeHRM）
- 关注 pytest-reportlog 的 Issue 区，看看有没有 good first issue
- 按学习路线继续推进，阶段一（测试理论）→ 阶段二（工具）
