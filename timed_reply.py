"""
多账户定时回复脚本 - 支持多个账户对多个链接进行定时回复
"""
import time
import logging
import os
import sys
import json
import threading
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 导入笑话生成模块
sys.path.append(os.path.join(os.path.dirname(__file__), 'content', 'joke_stories'))
try:
    from joke_generator import JokeGenerator
    JOKE_GENERATOR_AVAILABLE = True
except ImportError as e:
    print(f"警告: 无法导入笑话生成模块: {e}")
    JOKE_GENERATOR_AVAILABLE = False

class ConfigManager:
    """配置文件管理器"""
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {self.config_file} 不存在，请先创建配置文件")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            sys.exit(1)
    
    def get_enabled_accounts(self):
        """获取启用的账户列表"""
        return [account for account in self.config['accounts'] if account.get('enabled', True)]
    
    def get_enabled_targets(self, account):
        """获取账户下启用的回复目标列表"""
        return [target for target in account.get('reply_targets', []) if target.get('enabled', True)]

class TimedReplyBot:
    def __init__(self, config_manager):
        """
        初始化定时回复机器人
        
        Args:
            config_manager: 配置管理器实例
        """
        self.config_manager = config_manager
        self.config = config_manager.config
        self.drivers = {}  # 存储每个账户的浏览器驱动
        self.reply_stats = {}  # 存储每个账户的回复统计
        self.running = False
        self.threads = []
        
        # 工作时间配置（从配置文件中读取，默认 8:00-23:00 工作日）
        self.work_hours = self.config.get('work_hours', {
            'start_hour': 8,
            'end_hour': 23,
            'weekdays_only': True  # 仅工作日
        })
        
        # 初始化笑话生成器
        if JOKE_GENERATOR_AVAILABLE:
            self.joke_generator = JokeGenerator()
            self.logger = logging.getLogger(__name__)
            self.logger.info("笑话生成器已启用")
        else:
            self.joke_generator = None
            self.logger = logging.getLogger(__name__)
            self.logger.warning("笑话生成器不可用，将使用默认回复模板")
        
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO').upper())
        
        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # 文件处理器
        file_handler = logging.FileHandler(
            log_config.get('file', 'timed_reply.log'), 
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 配置根日志器
        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler]
        )
        self.logger = logging.getLogger(__name__)
    
    def is_within_work_hours(self):
        """检查当前时间是否在工作时间内"""
        now = datetime.now()
        current_hour = now.hour
        current_weekday = now.weekday()  # 0=周一, 6=周日
        
        start_hour = self.work_hours.get('start_hour', 8)
        end_hour = self.work_hours.get('end_hour', 23)
        weekdays_only = self.work_hours.get('weekdays_only', True)
        
        # 检查是否工作日
        if weekdays_only and current_weekday >= 5:  # 周六、周日
            self.logger.debug(f"当前是周末（周{current_weekday+1}），不在工作时间内")
            return False
        
        # 检查是否在时间范围内
        if current_hour < start_hour or current_hour >= end_hour:
            self.logger.debug(f"当前时间 {current_hour} 不在工作时间范围内（{start_hour}-{end_hour}）")
            return False
        
        return True
    
    def init_driver(self, account_id):
        """为指定账户初始化浏览器驱动"""
        browser_config = self.config.get('browser', {})
        chrome_options = Options()
        
        if browser_config.get('headless', True):
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument(f'--user-agent={browser_config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'--window-size={browser_config.get("window_size", "1920,1080")}')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            self.drivers[account_id] = driver
            self.logger.info(f"账户 {account_id} 浏览器驱动初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"账户 {account_id} 浏览器驱动初始化失败: {e}")
            return False
    
    def login(self, account):
        """登录指定账户"""
        account_id = account['id']
        username = account['username']
        password = account['password']
        
        if account_id not in self.drivers:
            if not self.init_driver(account_id):
                return False
        
        driver = self.drivers[account_id]
        forum_url = self.config['forum']['base_url']
        
        try:
            self.logger.info(f"账户 {account_id} 开始登录: {username}")
            driver.get(f"{forum_url}/member.php?mod=logging&action=login")
            time.sleep(3)
            
            # 等待登录表单加载
            wait = WebDriverWait(driver, 10)
            
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
                    self.logger.info(f"账户 {account_id} 找到用户名输入框: {selector_type}={selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not username_input:
                self.logger.error(f"账户 {account_id} 未找到用户名输入框")
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
                    password_input = driver.find_element(selector_type, selector_value)
                    self.logger.info(f"账户 {account_id} 找到密码输入框: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_input:
                self.logger.error(f"账户 {account_id} 未找到密码输入框")
                return False
            
            # 输入用户名和密码
            self.logger.info(f"账户 {account_id} 输入用户名: {username}")
            username_input.clear()
            username_input.send_keys(username)
            
            self.logger.info(f"账户 {account_id} 输入密码")
            password_input.clear()
            password_input.send_keys(password)
            
            # 处理安全提问字段（如果存在）
            try:
                security_selectors = [
                    (By.NAME, "questionid"),
                    (By.ID, "questionid"),
                    (By.CSS_SELECTOR, "select[name='questionid']")
                ]
                
                for selector_type, selector_value in security_selectors:
                    try:
                        security_element = driver.find_element(selector_type, selector_value)
                        from selenium.webdriver.support.ui import Select
                        select = Select(security_element)
                        if len(select.options) > 0:
                            select.select_by_index(0)
                            self.logger.info(f"账户 {account_id} 处理安全提问字段")
                        break
                    except:
                        continue
            except Exception as e:
                self.logger.debug(f"账户 {account_id} 安全提问字段处理: {e}")
            
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
                    login_button = driver.find_element(selector_type, selector_value)
                    self.logger.info(f"账户 {account_id} 找到登录按钮: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                self.logger.error(f"账户 {account_id} 未找到登录按钮")
                return False
            
            # 点击登录按钮
            self.logger.info(f"账户 {account_id} 点击登录按钮")
            login_button.click()
            
            # 等待登录完成
            time.sleep(5)
            
            # 检查是否登录成功
            page_source = driver.page_source
            success_indicators = [
                "欢迎",
                "退出", 
                "logout",
                "个人中心",
                "我的",
                username
            ]
            
            login_success = False
            for indicator in success_indicators:
                if indicator in page_source:
                    self.logger.info(f"账户 {account_id} 登录成功，找到指示器: {indicator}")
                    login_success = True
                    break
            
            if not login_success:
                self.logger.error(f"账户 {account_id} 登录失败")
                return False
            else:
                self.logger.info(f"账户 {account_id} 登录成功")
                return True
                
        except Exception as e:
            self.logger.error(f"账户 {account_id} 登录过程错误: {e}")
            return False
    
    def get_reply_message(self, target):
        """生成回复消息（支持笑话生成和模板）"""
        # 检查是否启用笑话生成
        joke_config = target.get('joke_generation', {})
        if joke_config.get('enabled', False) and self.joke_generator:
            try:
                # 获取笑话生成配置
                category = joke_config.get('category', 'any')
                format_type = joke_config.get('format', 'story_format')
                
                # 生成笑话
                joke_message = self.joke_generator.generate_joke_text(
                    count=1,
                    format_type=format_type,
                    category=category,
                    include_metadata=joke_config.get('include_metadata', False)
                )
                
                # 如果配置了笑话前缀或后缀，添加它们
                prefix = joke_config.get('prefix', '')
                suffix = joke_config.get('suffix', '')
                
                if prefix:
                    joke_message = f"{prefix}\n\n{joke_message}"
                if suffix:
                    joke_message = f"{joke_message}\n\n{suffix}"
                
                self.logger.info(f"使用笑话生成器生成回复消息，类别: {category}, 格式: {format_type}")
                return joke_message
                
            except Exception as e:
                self.logger.error(f"笑话生成失败，回退到模板模式: {e}")
                # 如果笑话生成失败，回退到模板模式
        
        # 使用传统模板模式
        templates = target.get('reply_templates', [])
        if not templates:
            return f"我在认真的水帖, - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 随机选择一个模板
        template = random.choice(templates)
        
        # 处理模板格式（支持新旧格式）
        if isinstance(template, dict):
            content = template.get('content', '')
        else:
            content = template
        
        # 替换时间戳占位符
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = content.replace('{timestamp}', timestamp)
        
        return message
    
    
    def post_reply(self, account_id, target):
        """发布回复"""
        driver = self.drivers.get(account_id)
        if not driver:
            self.logger.error(f"账户 {account_id} 浏览器驱动不存在")
            return False
        
        try:
            # 访问目标帖子
            self.logger.info(f"账户 {account_id} 访问目标帖子: {target['url']}")
            driver.get(target['url'])
            time.sleep(2)
            
            # 生成回复消息
            message = self.get_reply_message(target)
            
            # 查找快速回复框
            try:
                reply_textarea = driver.find_element(By.ID, "fastpostmessage")
                reply_textarea.clear()
                reply_textarea.send_keys(message)
                
                # 点击快速回复按钮
                reply_button = driver.find_element(By.ID, "fastpostsubmit")
                reply_button.click()
                
                time.sleep(2)
                
                # 更新统计信息
                if account_id not in self.reply_stats:
                    self.reply_stats[account_id] = {
                        'total_replies': 0,
                        'last_reply_time': None,
                        'start_time': datetime.now()
                    }
                
                self.reply_stats[account_id]['total_replies'] += 1
                self.reply_stats[account_id]['last_reply_time'] = datetime.now()
                
                self.logger.info(f"账户 {account_id} 成功发布回复 #{self.reply_stats[account_id]['total_replies']}: {message}")
                return True
                
            except NoSuchElementException:
                self.logger.warning(f"账户 {account_id} 未找到快速回复框，尝试其他方式")
                # 尝试查找其他可能的回复框
                try:
                    # 尝试查找普通回复框
                    reply_textarea = driver.find_element(By.CSS_SELECTOR, "textarea[name='message']")
                    reply_textarea.clear()
                    reply_textarea.send_keys(message)
                    
                    # 查找提交按钮
                    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    submit_button.click()
                    
                    time.sleep(2)
                    
                    # 更新统计信息
                    if account_id not in self.reply_stats:
                        self.reply_stats[account_id] = {
                            'total_replies': 0,
                            'last_reply_time': None,
                            'start_time': datetime.now()
                        }
                    
                    self.reply_stats[account_id]['total_replies'] += 1
                    self.reply_stats[account_id]['last_reply_time'] = datetime.now()
                    
                    self.logger.info(f"账户 {account_id} 成功发布回复 #{self.reply_stats[account_id]['total_replies']} (备用方法): {message}")
                    return True
                    
                except NoSuchElementException:
                    self.logger.error(f"账户 {account_id} 未找到回复框")
                    return False
                
        except Exception as e:
            self.logger.error(f"账户 {account_id} 发布回复失败: {e}")
            return False
    
    def display_stats(self):
        """显示统计信息"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 120)
        print("🤖 多账户定时回复机器人 - 统计信息")
        print("=" * 120)
        
        for account in self.config_manager.get_enabled_accounts():
            account_id = account['id']
            username = account['username']
            stats = self.reply_stats.get(account_id, {})
            
            print(f"\n👤 账户: {username} ({account_id})")
            print(f"📊 总回复数: {stats.get('total_replies', 0)}")
            
            if stats.get('last_reply_time'):
                print(f"🕐 最后回复: {stats['last_reply_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 显示该账户的回复目标
            targets = self.config_manager.get_enabled_targets(account)
            for target in targets:
                print(f"\n  📌 {target['name']}")
                print(f"     🔗 链接: {target['url']}")
                print(f"     ⏱️  间隔: {target['interval_seconds']}秒")
                
                # 显示开始延迟
                start_delay = target.get('start_delay_seconds', 0)
                if start_delay > 0:
                    print(f"     ⏳ 开始延迟: {start_delay}秒")
                else:
                    print(f"     ⏳ 开始延迟: 立即开始")
                
                # 显示笑话生成状态
                joke_config = target.get('joke_generation', {})
                if joke_config.get('enabled', False):
                    category = joke_config.get('category', 'any')
                    format_type = joke_config.get('format', 'story_format')
                    print(f"     😄 笑话生成: 启用 (类别: {category}, 格式: {format_type})")
                    
                    prefix = joke_config.get('prefix', '')
                    suffix = joke_config.get('suffix', '')
                    if prefix or suffix:
                        print(f"     📝 前缀/后缀: {prefix}...{suffix}")
                else:
                    print(f"     😄 笑话生成: 禁用")
                
                # 显示模板概要（仅当笑话生成禁用时显示）
                if not joke_config.get('enabled', False):
                    templates = target.get('reply_templates', [])
                    print(f"     📝 模板概要 ({len(templates)}个，随机选择):")
                    
                    for i, template in enumerate(templates):
                        # 处理模板格式
                        if isinstance(template, dict):
                            content = template.get('content', '')
                        else:
                            content = template
                        
                        # 截断过长的内容
                        display_content = content[:50] + "..." if len(content) > 50 else content
                        print(f"       {i+1}. {display_content}")
                else:
                    print(f"     📝 回复模式: 笑话生成模式")
        
        print("\n" + "=" * 120)
        print("按 Ctrl+C 停止机器人")
        print("=" * 120)
    
    def run_account_target(self, account, target):
        """运行单个账户的单个目标"""
        account_id = account['id']
        target_id = target['id']
        interval_seconds = target['interval_seconds']
        start_delay = target.get('start_delay_seconds', 0)
        
        self.logger.info(f"启动账户 {account_id} 的目标 {target_id}，间隔 {interval_seconds} 秒，延迟 {start_delay} 秒")
        
        # 登录账户
        if not self.login(account):
            self.logger.error(f"账户 {account_id} 登录失败，跳过目标 {target_id}")
            return
        
        # 开始延迟
        if start_delay > 0:
            self.logger.info(f"账户 {account_id} 目标 {target_id} 延迟 {start_delay} 秒后开始")
            for i in range(start_delay, 0, -1):
                if not self.running:
                    return
                time.sleep(1)
                if i % 10 == 0:  # 每10秒显示一次统计
                    self.display_stats()
        
        while self.running:
            try:
                # 发布回复
                success = self.post_reply(account_id, target)
                if not success:
                    self.logger.error(f"账户 {account_id} 目标 {target_id} 回复失败")
                
                # 等待指定时间
                for i in range(interval_seconds, 0, -1):
                    if not self.running:
                        break
                    
                    # 检查是否在工作时间内
                    if not self.is_within_work_hours():
                        self.logger.info(f"账户 {account_id} 目标 {target_id} 不在工作时间内，停止运行")
                        self.running = False
                        break
                    
                    time.sleep(1)
                    
                    # 每10秒显示一次统计信息
                    if i % 10 == 0:
                        self.display_stats()
                
            except Exception as e:
                self.logger.error(f"账户 {account_id} 目标 {target_id} 运行错误: {e}")
                time.sleep(30)  # 出错后等待30秒再重试
    
    def run_timed_reply(self):
        """运行多账户定时回复任务"""
        self.logger.info("启动多账户定时回复任务")
        
        # 检查是否在工作时间内
        if not self.is_within_work_hours():
            now = datetime.now()
            self.logger.info(f"当前时间 {now.strftime('%Y-%m-%d %H:%M:%S')} 不在工作时间内，退出")
            return
        
        self.running = True
        
        # 获取启用的账户
        enabled_accounts = self.config_manager.get_enabled_accounts()
        if not enabled_accounts:
            self.logger.error("没有启用的账户")
            return
        
        self.logger.info(f"找到 {len(enabled_accounts)} 个启用的账户")
        
        # 为每个账户的每个目标创建线程
        for account in enabled_accounts:
            account_id = account['id']
            username = account['username']
            
            # 获取该账户启用的目标
            enabled_targets = self.config_manager.get_enabled_targets(account)
            if not enabled_targets:
                self.logger.warning(f"账户 {username} 没有启用的回复目标")
                continue
            
            self.logger.info(f"账户 {username} 有 {len(enabled_targets)} 个启用的回复目标")
            
            # 为每个目标创建线程
            for target in enabled_targets:
                thread = threading.Thread(
                    target=self.run_account_target,
                    args=(account, target),
                    name=f"{account_id}_{target['id']}"
                )
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
        
        try:
            # 主循环显示统计信息
            while self.running:
                # 检查是否仍在工作时间内
                if not self.is_within_work_hours():
                    now = datetime.now()
                    self.logger.info(f"到达工作时间结束时间 {now.strftime('%Y-%m-%d %H:%M:%S')}，停止运行")
                    self.running = False
                    break
                
                self.display_stats()
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.logger.info("收到停止信号")
            self.running = False
            
            # 等待所有线程结束
            for thread in self.threads:
                thread.join(timeout=5)
            
            # 显示最终统计
            print("\n🤖 机器人已停止！")
            for account in enabled_accounts:
                account_id = account['id']
                username = account['username']
                stats = self.reply_stats.get(account_id, {})
                print(f"账户 {username}: 总回复数 {stats.get('total_replies', 0)}")
        
        finally:
            self.close_all_drivers()
    
    def close_all_drivers(self):
        """关闭所有浏览器驱动"""
        for account_id, driver in self.drivers.items():
            try:
                driver.quit()
                self.logger.info(f"账户 {account_id} 浏览器已关闭")
            except Exception as e:
                self.logger.error(f"关闭账户 {account_id} 浏览器时出错: {e}")

def main():
    """主函数"""
    # 创建配置管理器
    config_manager = ConfigManager('config.json')
    
    # 创建定时回复机器人
    bot = TimedReplyBot(config_manager)
    
    # 运行定时回复任务
    bot.run_timed_reply()

if __name__ == "__main__":
    main()