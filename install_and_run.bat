@echo off
chcp 65001
echo ========================================
echo ZelosTech 论坛自动化工具
echo ========================================
echo.

echo 正在检查 Python 环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo 依赖包安装完成！
echo.
echo 正在启动论坛自动化工具...
python run_local.py

pause
