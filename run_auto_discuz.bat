@echo off
chcp 65001 >nul
echo ========================================
echo ZelosTech 论坛自动化工具
echo ========================================
echo.

echo 正在检查Python环境...
C:\Users\syt89\AppData\Local\Programs\Python\Python313\python.exe --version
if errorlevel 1 (
    echo [ERROR] Python未找到，请检查Python安装
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
C:\Users\syt89\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo [OK] 依赖包安装完成
echo.

echo 请确认您的论坛配置信息：
echo - 论坛地址: http://bbs.zelostech.com.cn
echo - 用户名: yurisun
echo - 密码: sunyuting0
echo.
echo 如果信息不正确，请修改 config.py 文件中的配置
echo.

pause

echo 启动论坛自动化...
C:\Users\syt89\AppData\Local\Programs\Python\Python313\python.exe run_local.py

pause

