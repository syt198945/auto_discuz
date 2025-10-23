@echo off
chcp 65001 >nul
echo ========================================
echo Discuz 论坛登录调试工具
echo ========================================
echo.

echo 正在启动登录调试工具...
echo 注意：此工具会打开浏览器窗口进行调试
echo.

C:\Users\syt89\AppData\Local\Programs\Python\Python313\python.exe test_login_debug.py

echo.
echo 调试完成
pause

