# 软件测试开源项目推荐

> 适合零经验初学者参与的开源项目
> 参与开源是弥补"没有工作经验"的最佳方式

---

## 📌 使用策略

在参与这些项目之前，先明确你的目标：

1. **不要一上来就想着提交代码**——先读文档、跑项目、写测试用例
2. **从 Issue 列表里的 "good first issue" 或 "help wanted" 标签开始**
3. **给现有项目加测试用例是最好的入门方式**——这是实打实的测试工作
4. **把参与过程记下来，写进简历**

---

## 🔷 第一类：自己搭建练习目标（推荐先做）

> 这些项目你 Fork 到本地，用来练习写测试用例。

### 1. 简单的 Web 应用 — Flask TODO

```bash
# 从 GitHub 克隆一个最简单的 TODO 应用作为测试目标
git clone https://github.com/amcerbu/Flask-Todo.git
cd Flask-Todo
pip install -r requirements.txt
python app.py
```
- **练习内容**：对这个 TODO 应用编写功能测试用例（手工 + 自动化）
- **技术栈**：Python + Flask + HTML
- **难度**：⭐⭐ （非常简单）

### 2. JSONPlaceholder — 模拟 API

- 地址：https://jsonplaceholder.typicode.com
- **练习内容**：用 Postman 和 pytest 对这个模拟 API 做接口测试
- **特点**：不需要搭建环境，直接在线请求即可
- **难度**：⭐

### 3. Swagger Petstore — 宠物商店 API

- 地址：https://petstore.swagger.io
- **练习内容**：对标准的 REST API 做接口测试，覆盖所有端点的正常和异常场景
- **难度**：⭐⭐

---

## 🔷 第二类：给 Python 开源项目贡献测试用例

> 这些是真实的 Python 开源项目，仓库里通常缺少测试覆盖，恰好需要贡献者帮忙补测试。

### 1. HTTPBin（★★★★★ 强烈推荐）

- GitHub：https://github.com/postmanlabs/httpbin
- 语言：Python（Flask）
- **为什么适合你**：
  - HTTPBin 本身就是一个测试工具，代码量不大，容易理解
  - 项目有测试（tests/ 目录），可以直接参考现有测试写新的
  - 即使不提交 PR，拿它练习写 pytest 测试脚本也是极好的
- **找 Issue**：进 Issues → 搜索 "good first issue" 或 "test coverage"

### 2. Click（Python 命令行库）

- GitHub：https://github.com/pallets/click
- 语言：Python
- **为什么适合**：
  - Pallets 项目（Flask 的团队）对贡献者友好
  - Click 的测试基础设施完善，容易上手
  - 可以在文档或测试用例方面贡献
- **入门**：阅读 CONTRIBUTING.md → 找带 "good first issue" 标签的 Issue

### 3. Rich（Python 终端富文本库）

- GitHub：https://github.com/Textualize/rich
- 语言：Python
- **为什么适合**：
  - 非常活跃的开源项目，社区友好
  - 有许多 "good first issue" 标签的任务
  - 测试框架用的是 pytest，和你需要学的框架一致

---

## 🔷 第三类：专业的开源测试项目

> 这些是测试领域的开源项目本身，参与它们既能学测试，也能接触到真实的测试工具生态。

### 1. ❤️ Pytest（★★★ 推荐了解）

- GitHub：https://github.com/pytest-dev/pytest
- 简介：Python 最流行的测试框架，几乎所有 Python 测试都绕不开它
- **如何参与**：
  - 阅读官方文档，帮助完善中文翻译
  - 写一些示例代码放到 examples/ 目录
  - 找 "good first issue" 解决简单问题
- **对你简历的价值**：如果在简历里写"为 pytest 贡献过文档/测试"，面试官会高看一眼

### 2. HTTPRunner（★★★★★ 强烈推荐）

- GitHub：https://github.com/httprunner/httprunner
- 简介：一款优雅的 API 测试工具，支持 YAML/JSON 格式的测试用例
- **语言**：Python
- **为什么适合你**：
  - 国内项目，中文文档完善，社区以中文为主
  - 本身就是测试工具，参与它能学到 API 测试的最佳实践
  - 项目有 "good first issue" 标签
- **入门**：Fork → 阅读文档 → 跑测试 → 查看 Issue

### 3. Metersphere（★★★ 推荐）

- GitHub：https://github.com/metersphere/metersphere
- 简介：一站式的开源持续测试平台，支持接口测试、UI 测试、性能测试
- **语言**：Java 后端 + Vue 前端
- **适合人群**：如果以后想接触更完整的测试平台生态
- **注意**：项目比较大，建议先从文档阅读开始

### 4. Selenium HQ（★★★ 了解即可）

- GitHub：https://github.com/SeleniumHQ/selenium
- 简介：Web UI 自动化测试的老牌项目
- **如何参与**：
  - 帮助完善 Python 绑定的文档
  - 编写示例代码
  - 提交 Bug 报告也是一种贡献
- **难度**：⭐⭐⭐⭐（代码量大，但文档贡献门槛低）

### 5. Locust（★★★★ 推荐）

- GitHub：https://github.com/locustio/locust
- 简介：Python 性能测试工具，用代码定义用户行为
- **语言**：Python
- **为什么适合**：
  - 代码量适中，结构清晰
  - 性能测试是面试加分项
  - 社区活跃，Issue 回复快

---

## 🔷 第四类：测试练习靶场（练手专用）

> 这些不是开源项目，而是专门给你"练手测试"的网站，不需要自己搭环境。

### 1. 测试练习网站
| 网站 | 地址 | 练习内容 |
|------|------|----------|
| Sauce Demo | https://www.saucedemo.com | 电商网站，可以练 UI 自动化测试 |
| Para Bank | https://parabank.parasoft.com | 银行系统，可以练功能测试 |
| OrangeHRM | https://opensource-demo.orangehrmlive.com | 人事管理系统，功能丰富 |
| Swag Labs | https://www.saucedemo.com | Sauce Demo 的另一个版本 |

### 2. Bug 寻找练习
| 网站 | 地址 | 说明 |
|------|------|------|
| Testbirds | https://www.testbirds.com | 众包测试平台 |
| uTest | https://www.utest.com | 全球最大的众包测试平台，注册后可接真实测试任务 |
| 阿里众包 | 搜索"阿里众包 测试" | 国内平台，有测试任务 |

---

## 🔷 第五类：适合中国求职者的中文开源项目

| 项目 | 地址 | 推荐理由 |
|------|------|----------|
| 接口测试平台 | https://github.com/zhangfei19841004/zat | 接口测试管理平台 |
| Sonic | https://github.com/SonicCloudOrg/sonic | 云真机测试平台（自动化测试） |
| LuckyFrame | https://gitee.com/seagull1985/LuckyFrame | 自动化测试平台，中文生态 |

---

## 📋 推荐行动计划（按优先级排序）

```
优先级 ⭐⭐⭐⭐⭐
  1. Fork HTTPBin → 阅读源码 → 用 pytest 写新的测试用例
  2. 参与 HttpRunner → 读文档 → 找 good first issue
  3. 用 Sauce Demo 练 Selenium 自动化

优先级 ⭐⭐⭐⭐
  4. 关注 Pytest 项目 → 看 Issue → 从文档/示例贡献开始
  5. 用 Flask-Todo 搭建自己的练习目标 → 写完整测试套件

优先级 ⭐⭐⭐
  6. 注册 uTest 平台 → 接真实任务
  7. 尝试贡献 Rich / Click 等项目
```

---

## 💡 如何把参与开源写进简历

```markdown
### 开源项目贡献 — HttpRunner

- 为 HttpRunner 项目提交了 2 个测试用例的 PR，覆盖异常参数输入场景
- 阅读项目源码并理解了 API 测试框架的核心设计
- 在项目 Issue 区参与讨论，提交了 1 个有效的 Bug 报告
```

即使你的 PR 没有被合并，只要你认真做了，面试时提起也能展示你的**主动性**和**技术热情**。
