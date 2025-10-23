@echo off
echo ========================================
echo 🤖 TIMED REPLY BOT
echo ========================================
echo Target Post: http://bbs.zelostech.com.cn/forum.php?mod=viewthread^&tid=37^&extra=page%%3D1
echo Reply Interval: 15 seconds
echo Features: Dynamic stats, countdown timer
echo Press Ctrl+C to stop the bot
echo ========================================
echo.

py -3.13 timed_reply.py

echo.
echo Bot has stopped. Press any key to exit...
pause
