"""
定时回复脚本 - 每隔15秒向指定帖子发布带时间戳的消息
"""
import time
import logging
import os
import sys
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config

class TimedReplyBot:
    def __init__(self, target_url, interval_seconds=15):
        """
        初始化定时回复机器人
        
        Args:
            target_url: 目标帖子URL
            interval_seconds: 回复间隔（秒），默认15秒
        """
        self.config = Config()
        self.target_url = target_url
        self.interval_seconds = interval_seconds
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
                logging.FileHandler('timed_reply.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_driver(self):
        """初始化浏览器驱动"""
        chrome_options = Options()
        if self.config.HEADLESS:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--user-agent={self.config.USER_AGENT}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
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
            
            # 处理安全提问字段（如果存在）
            try:
                security_selectors = [
                    (By.NAME, "questionid"),
                    (By.ID, "questionid"),
                    (By.CSS_SELECTOR, "select[name='questionid']")
                ]
                
                for selector_type, selector_value in security_selectors:
                    try:
                        security_element = self.driver.find_element(selector_type, selector_value)
                        from selenium.webdriver.support.ui import Select
                        select = Select(security_element)
                        if len(select.options) > 0:
                            select.select_by_index(0)
                            self.logger.info("Security question field handled")
                        break
                    except:
                        continue
            except Exception as e:
                self.logger.debug(f"Security question field handling: {e}")
            
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
        message = f"Auto reply - Timestamp: {timestamp}"
        return message
    
    def display_stats(self, next_reply_time=None):
        """显示统计信息"""
        if self.start_time is None:
            self.start_time = datetime.now()
        
        current_time = datetime.now()
        runtime = current_time - self.start_time
        
        # 计算运行时间
        hours, remainder = divmod(runtime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # 计算平均回复间隔
        avg_interval = 0
        if self.reply_count > 0:
            avg_interval = runtime.total_seconds() / self.reply_count
        
        # 清屏并显示统计信息
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("🤖 TIMED REPLY BOT - STATISTICS")
        print("=" * 80)
        print(f"📊 Target Post: {self.target_url}")
        print(f"⏱️  Reply Interval: {self.interval_seconds} seconds")
        print(f"📈 Total Replies: {self.reply_count}")
        print(f"⏰ Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        print(f"📊 Average Interval: {avg_interval:.1f} seconds")
        
        if self.last_reply_time:
            print(f"🕐 Last Reply: {self.last_reply_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if next_reply_time:
            print(f"⏳ Next Reply: {next_reply_time.strftime('%Y-%m-%d %H:%M:%S')}")
            remaining = (next_reply_time - current_time).total_seconds()
            print(f"⏱️  Time Remaining: {remaining:.0f} seconds")
        
        print("=" * 80)
        print("Press Ctrl+C to stop the bot")
        print("=" * 80)
    
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
                    
                except NoSuchElementException:
                    self.logger.error("No reply box found")
                    return False
                
        except Exception as e:
            self.logger.error(f"Failed to post reply: {e}")
            return False
    
    def run_timed_reply(self):
        """运行定时回复任务"""
        self.logger.info("Starting timed reply task")
        self.logger.info(f"Target post: {self.target_url}")
        self.logger.info(f"Reply interval: {self.interval_seconds} seconds")
        
        # 登录
        if not self.login():
            self.logger.error("Login failed, cannot continue")
            return
        
        try:
            while True:
                # 计算下一次回复时间
                next_reply_time = datetime.now() + timedelta(seconds=self.interval_seconds)
                
                # 显示统计信息
                self.display_stats(next_reply_time)
                
                # 生成带时间戳的消息
                message = self.get_timestamp_message()
                
                # 发布回复
                success = self.post_reply(message)
                if not success:
                    self.logger.error(f"Reply #{self.reply_count + 1} failed")
                
                # 等待指定时间，同时显示倒计时
                self.countdown_wait(self.interval_seconds)
                
        except KeyboardInterrupt:
            self.logger.info(f"Received stop signal, total replies posted: {self.reply_count}")
            print(f"\n🤖 Bot stopped! Total replies: {self.reply_count}")
        except Exception as e:
            self.logger.error(f"Error during execution: {e}")
        finally:
            self.close()
    
    def countdown_wait(self, seconds):
        """带倒计时的等待"""
        for i in range(seconds, 0, -1):
            next_reply_time = datetime.now() + timedelta(seconds=i-1)
            self.display_stats(next_reply_time)
            time.sleep(1)
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")

def main():
    """主函数"""
    # 目标帖子URL
    target_url = "http://bbs.zelostech.com.cn/forum.php?mod=viewthread&tid=37&extra=page%3D1"
    
    # 创建定时回复机器人
    bot = TimedReplyBot(target_url, interval_seconds=15)
    
    # 运行定时回复任务
    bot.run_timed_reply()

if __name__ == "__main__":
    main()
