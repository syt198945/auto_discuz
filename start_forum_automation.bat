@echo off
chcp 65001
title ZelosTech 论坛自动化工具

echo ========================================
echo ZelosTech 论坛自动化工具
echo ========================================
echo.

echo 正在检查 Python 环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python
    echo 请先安装 Python 3.8+ 并添加到 PATH
    pause
    exit /b 1
)

echo.
echo 正在安装基础依赖包...
python -m pip install --upgrade pip
python -m pip install requests beautifulsoup4

echo.
echo 正在测试论坛连接...
python simple_forum_test.py

echo.
echo 按任意键继续...
pause > nul
