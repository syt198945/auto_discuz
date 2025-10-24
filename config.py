"""
Discuz 论坛自动化配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 论坛基本信息
    FORUM_URL = os.getenv('FORUM_URL', 'http://bbs.zelostech.com.cn')
    FORUM_NAME = os.getenv('FORUM_NAME', 'ZelosTech论坛')
    
    # 登录信息
    USERNAME = os.getenv('FORUM_USERNAME', '孙玉铤')
    PASSWORD = os.getenv('FORUM_PASSWORD', 'zaq1@WSX')
    
    # 登录方式选择
    LOGIN_METHOD = os.getenv('LOGIN_METHOD', 'feishu')  # 'feishu' 或 'password'
    
    # 飞书登录配置
    FEISHU_LOGIN_ENABLED = os.getenv('FEISHU_LOGIN_ENABLED', 'true').lower() == 'true'
    FEISHU_LOGIN_URL = os.getenv('FEISHU_LOGIN_URL', '/plugin.php?id=feishulogin:login')
    
    # 飞书API配置
    FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', '')
    FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', '')
    FEISHU_REDIRECT_URI = os.getenv('FEISHU_REDIRECT_URI', '/plugin.php?id=feishulogin:callback&action=login')
    
    # 自动化设置
    AUTO_REPLY_ENABLED = os.getenv('AUTO_REPLY_ENABLED', 'true').lower() == 'true'
    AUTO_CREATE_TOPIC_ENABLED = os.getenv('AUTO_CREATE_TOPIC_ENABLED', 'true').lower() == 'true'
    
    # 定时任务设置
    REPLY_CHECK_INTERVAL = int(os.getenv('REPLY_CHECK_INTERVAL', '300'))  # 5分钟
    TOPIC_CREATE_SCHEDULE = os.getenv('TOPIC_CREATE_SCHEDULE', '09:00,15:00,21:00')  # 每天3次
    
    # 回复模板 - 针对技术论坛
    REPLY_TEMPLATES = [
        "感谢分享，很有用的技术信息！",
        "学习了，谢谢楼主的分享！",
        "这个技术方案很有意思，我也有类似的经验。",
        "支持楼主，期待更多技术干货！",
        "感谢楼主分享，收藏学习了！",
        "这个思路不错，值得借鉴！",
        "技术交流很有价值，感谢分享！",
        "学到了，谢谢楼主的详细说明！",
        "这个解决方案很实用，赞一个！",
        "技术讨论很有意义，继续加油！"
    ]
    
    # 主题模板 - 针对ZelosTech论坛
    TOPIC_TEMPLATES = [
        {
            "title": "技术交流分享",
            "content": "大家好，今天想和大家分享一些技术心得和开发经验，欢迎大家一起讨论交流！",
            "forum_id": "1"  # 根据论坛结构调整
        },
        {
            "title": "项目开发讨论",
            "content": "最近在开发一个项目，遇到了一些技术问题，想听听大家的建议和解决方案。",
            "forum_id": "1"
        },
        {
            "title": "学习心得分享",
            "content": "学习新技术的过程中有一些心得体会，想和大家分享，也希望能从大家那里学到更多。",
            "forum_id": "1"
        }
    ]
    
    # 浏览器设置
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # 日志设置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'forum_automation.log')
