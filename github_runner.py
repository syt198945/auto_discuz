#!/usr/bin/env python3
"""
GitHub Actions 运行器
专门为GitHub Actions环境优化的定时回复脚本
"""
import os
import sys
import time
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config

class GitHubTimedReplyBot:
    def __init__(self, target_url, interval_seconds=15, max_runtime_hours=1):
        """
        初始化GitHub定时回复机器人
        
        Args:
            target_url: 目标帖子URL
            interval_seconds: 回复间隔（秒），默认15秒
            max_runtime_hours: 最大运行时间（小时），默认1小时
        """
        self.config = Config()
        self.target_url = target_url
        self.interval_seconds = interval_seconds
        self.max_runtime_hours = max_runtime_hours
        self.driver = None
        self.reply_count = 0
        self.start_time = None
        self.last_reply_time = None
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('github_timed_reply.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_driver(self):
        """初始化浏览器驱动"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={self.config.USER_AGENT}')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.logger.info("Browser driver initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize browser driver: {e}")
            return False
    
    def login(self):
        """登录论坛"""
        if not self.driver:
            if not self.init_driver():
                return False
        
        try:
            self.logger.info(f"Accessing login page: {self.config.FORUM_URL}/member.php?mod=logging&action=login")
            self.driver.get(f"{self.config.FORUM_URL}/member.php?mod=logging&action=login")
            time.sleep(3)
            
            # 等待登录表单加载
            wait = WebDriverWait(self.driver, 10)
            
            # 查找用户名输入框
            username_input = None
            username_selectors = [
                (By.NAME, "username"),
                (By.NAME, "login_username"),
                (By.ID, "username"),
                (By.ID, "login_username")
            ]
            
            for selector_type, selector_value in username_selectors:
                try:
                    username_input = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                    self.logger.info(f"Found username input: {selector_type}={selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not username_input:
                self.logger.error("Username input not found")
                return False
            
            # 查找密码输入框
            password_input = None
            password_selectors = [
                (By.NAME, "password"),
                (By.NAME, "login_password"),
                (By.ID, "password"),
                (By.ID, "login_password")
            ]
            
            for selector_type, selector_value in password_selectors:
                try:
                    password_input = self.driver.find_element(selector_type, selector_value)
                    self.logger.info(f"Found password input: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_input:
                self.logger.error("Password input not found")
                return False
            
            # 输入用户名和密码
            self.logger.info(f"Entering username: {self.config.USERNAME}")
            username_input.clear()
            username_input.send_keys(self.config.USERNAME)
            
            self.logger.info("Entering password")
            password_input.clear()
            password_input.send_keys(self.config.PASSWORD)
            
            # 查找登录按钮
            login_button = None
            button_selectors = [
                (By.NAME, "loginsubmit"),
                (By.ID, "loginsubmit"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]
            
            for selector_type, selector_value in button_selectors:
                try:
                    login_button = self.driver.find_element(selector_type, selector_value)
                    self.logger.info(f"Found login button: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                self.logger.error("Login button not found")
                return False
            
            # 点击登录按钮
            self.logger.info("Clicking login button")
            login_button.click()
            
            # 等待登录完成
            time.sleep(5)
            
            # 检查是否登录成功
            page_source = self.driver.page_source
            success_indicators = [
                "欢迎",
                "退出", 
                "logout",
                "个人中心",
                "我的",
                self.config.USERNAME
            ]
            
            login_success = False
            for indicator in success_indicators:
                if indicator in page_source:
                    self.logger.info(f"Found login success indicator: {indicator}")
                    login_success = True
                    break
            
            if not login_success:
                self.logger.error("Login failed")
                return False
            else:
                self.logger.info("Login successful")
                return True
                
        except Exception as e:
            self.logger.error(f"Login process error: {e}")
            return False
    
    def get_timestamp_message(self):
        """生成带时间戳的消息"""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        message = f"🤖 GitHub Actions Auto Reply - {timestamp}"
        return message
    
    def post_reply(self, message):
        """发布回复"""
        try:
            # 访问目标帖子
            self.logger.info(f"访问目标帖子: {self.target_url}")
            self.driver.get(self.target_url)
            time.sleep(2)
            
            # 查找快速回复框
            try:
                reply_textarea = self.driver.find_element(By.ID, "fastpostmessage")
                reply_textarea.clear()
                reply_textarea.send_keys(message)
                
                # 点击快速回复按钮
                reply_button = self.driver.find_element(By.ID, "fastpostsubmit")
                reply_button.click()
                
                time.sleep(2)
                self.reply_count += 1
                self.last_reply_time = datetime.now()
                self.logger.info(f"Successfully posted reply #{self.reply_count}: {message}")
                return True
                
            except NoSuchElementException:
                self.logger.warning("未找到快速回复框，尝试其他方式")
                # 尝试查找其他可能的回复框
                try:
                    # 尝试查找普通回复框
                    reply_textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='message']")
                    reply_textarea.clear()
                    reply_textarea.send_keys(message)
                    
                    # 查找提交按钮
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    submit_button.click()
                    
                    time.sleep(2)
                    self.reply_count += 1
                    self.last_reply_time = datetime.now()
                    self.logger.info(f"Successfully posted reply #{self.reply_count} (alternative method): {message}")
                    return True
                    
                except NoElementException:
                    self.logger.error("No reply box found")
                    return False
                
        except Exception as e:
            self.logger.error(f"Failed to post reply: {e}")
            return False
    
    def run_timed_reply(self):
        """运行定时回复任务"""
        self.logger.info("Starting GitHub Actions timed reply task")
        self.logger.info(f"Target post: {self.target_url}")
        self.logger.info(f"Reply interval: {self.interval_seconds} seconds")
        self.logger.info(f"Max runtime: {self.max_runtime_hours} hours")
        
        # 登录
        if not self.login():
            self.logger.error("Login failed, cannot continue")
            return
        
        self.start_time = datetime.now()
        max_end_time = self.start_time + timedelta(hours=self.max_runtime_hours)
        
        try:
            while datetime.now() < max_end_time:
                # 生成带时间戳的消息
                message = self.get_timestamp_message()
                
                # 发布回复
                success = self.post_reply(message)
                if not success:
                    self.logger.error(f"Reply #{self.reply_count + 1} failed")
                
                # 计算剩余时间
                remaining_time = (max_end_time - datetime.now()).total_seconds()
                if remaining_time <= self.interval_seconds:
                    self.logger.info(f"Max runtime reached, stopping. Total replies: {self.reply_count}")
                    break
                
                # 等待指定时间
                self.logger.info(f"Waiting {self.interval_seconds} seconds until next reply...")
                time.sleep(self.interval_seconds)
                
        except Exception as e:
            self.logger.error(f"Error during execution: {e}")
        finally:
            self.close()
            self.logger.info(f"GitHub Actions bot finished. Total replies: {self.reply_count}")
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")

def main():
    """主函数"""
    # 从环境变量获取配置
    target_url = os.getenv('TARGET_URL', "http://bbs.zelostech.com.cn/forum.php?mod=viewthread&tid=37&extra=page%3D1")
    interval_seconds = int(os.getenv('INTERVAL_SECONDS', '15'))
    max_runtime_hours = int(os.getenv('MAX_RUNTIME_HOURS', '1'))
    
    # 创建GitHub定时回复机器人
    bot = GitHubTimedReplyBot(target_url, interval_seconds, max_runtime_hours)
    
    # 运行定时回复任务
    bot.run_timed_reply()

if __name__ == "__main__":
    main()
