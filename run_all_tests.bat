@echo off
chcp 65001 >nul
echo ============================================
echo  软件测试实战项目 — 一键安装与测试脚本
echo ============================================
echo.

REM 检测 Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.11+
    echo        下载地址: https://www.python.org/downloads/
    echo.
    echo 安装时务必勾选 "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo.

REM 给每个项目安装依赖并运行测试
set ROOT=%~dp0

echo ---------- 项目一：HTTPBin API 测试 ----------
cd /d "%ROOT%project_01_httpbin_tests"
pip install -r requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    pip install pytest requests pytest-html -q
)
echo 运行测试...
python -m pytest -v -m "not slow" --tb=short
echo.

echo ---------- 项目二：Flask TODO 功能测试 ----------
cd /d "%ROOT%project_02_flask_todo_tests"
pip install -r requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    pip install flask pytest pytest-html -q
)
echo 运行测试...
python -m pytest -v --tb=short
echo.

echo ---------- 项目三：Selenium UI 测试 ----------
cd /d "%ROOT%project_03_selenium_tests"
pip install -r requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    pip install selenium pytest pytest-html -q
)
echo 运行测试（无头模式）...
python -m pytest -v --tb=short
echo.

echo ============================================
echo  全部项目运行完成！
echo ============================================
echo.
echo 如果想生成 HTML 测试报告，可以分别运行：
echo   cd project_01_httpbin_tests ^&^& pytest --html=report.html --self-contained-html
echo   cd project_02_flask_todo_tests ^&^& pytest --html=report.html --self-contained-html
echo   cd project_03_selenium_tests ^&^& pytest --html=report.html --self-contained-html
echo.
pause
