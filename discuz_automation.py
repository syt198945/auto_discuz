"""
Discuz 论坛自动化核心模块
"""
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import Config

class DiscuzAutomation:
    def __init__(self):
        self.config = Config()
        self.driver = None
        self.session = requests.Session()
        self.setup_logging()
        self.setup_session()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_session(self):
        """设置请求会话"""
        ua = UserAgent()
        self.session.headers.update({
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
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
            self.logger.info("浏览器驱动初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"浏览器驱动初始化失败: {e}")
            return False
    
    def login(self):
        """登录论坛"""
        if not self.driver:
            if not self.init_driver():
                return False
        
        try:
            self.logger.info(f"访问登录页面: {self.config.FORUM_URL}/member.php?mod=logging&action=login")
            self.driver.get(f"{self.config.FORUM_URL}/member.php?mod=logging&action=login")
            time.sleep(3)
            
            self.logger.info(f"当前页面标题: {self.driver.title}")
            self.logger.info(f"当前页面URL: {self.driver.current_url}")
            
            # 等待登录表单加载，尝试多种选择器
            wait = WebDriverWait(self.driver, 10)
            
            # 尝试多种可能的用户名输入框选择器
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
                    self.logger.info(f"找到用户名输入框: {selector_type}={selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not username_input:
                self.logger.error("未找到用户名输入框")
                # 记录页面表单元素用于调试
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    self.logger.debug(f"页面输入框: {inp.get_attribute('outerHTML')}")
                return False
            
            # 尝试多种可能的密码输入框选择器
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
                    self.logger.info(f"找到密码输入框: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_input:
                self.logger.error("未找到密码输入框")
                return False
            
            # 输入用户名和密码
            self.logger.info(f"输入用户名: {self.config.USERNAME}")
            username_input.clear()
            username_input.send_keys(self.config.USERNAME)
            
            self.logger.info("输入密码")
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
                        # 如果找到安全提问下拉框，选择"无"或第一个选项
                        from selenium.webdriver.support.ui import Select
                        select = Select(security_element)
                        if len(select.options) > 0:
                            select.select_by_index(0)  # 选择第一个选项（通常是"无"）
                            self.logger.info("已处理安全提问字段")
                        break
                    except:
                        continue
            except Exception as e:
                self.logger.debug(f"安全提问字段处理: {e}")
            
            # 尝试多种可能的登录按钮选择器
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
                    self.logger.info(f"找到登录按钮: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                self.logger.error("未找到登录按钮")
                return False
            
            # 点击登录按钮
            self.logger.info("点击登录按钮")
            login_button.click()
            
            # 等待登录完成
            time.sleep(5)
            
            self.logger.info(f"登录后页面标题: {self.driver.title}")
            self.logger.info(f"登录后页面URL: {self.driver.current_url}")
            
            # 检查是否登录成功，使用多种标识
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
                    self.logger.info(f"找到登录成功标识: {indicator}")
                    login_success = True
                    break
            
            if not login_success:
                self.logger.error("未找到登录成功标识")
                
                # 检查是否有错误信息
                error_indicators = [
                    "用户名或密码错误",
                    "登录失败",
                    "密码错误",
                    "用户不存在",
                    "验证码错误"
                ]
                
                for error in error_indicators:
                    if error in page_source:
                        self.logger.error(f"找到错误信息: {error}")
                        break
                
                self.logger.debug(f"页面内容预览: {page_source[:500]}...")
                return False
            else:
                self.logger.info("登录成功")
                return True
                
        except Exception as e:
            self.logger.error(f"登录过程出错: {e}")
            return False
    
    def get_new_topics(self, forum_id=None, limit=10):
        """获取新主题列表"""
        try:
            url = f"{self.config.FORUM_URL}/forum.php"
            if forum_id:
                url += f"?mod=forumdisplay&fid={forum_id}"
            
            response = self.session.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            topics = []
            topic_elements = soup.find_all('tr', class_='new')[:limit]
            
            for element in topic_elements:
                try:
                    title_link = element.find('a', class_='s xst')
                    if title_link:
                        title = title_link.get_text().strip()
                        href = title_link.get('href')
                        if href and not href.startswith('http'):
                            href = self.config.FORUM_URL + '/' + href
                        
                        topics.append({
                            'title': title,
                            'url': href,
                            'forum_id': forum_id
                        })
                except Exception as e:
                    self.logger.warning(f"解析主题时出错: {e}")
                    continue
            
            self.logger.info(f"获取到 {len(topics)} 个新主题")
            return topics
            
        except Exception as e:
            self.logger.error(f"获取主题列表失败: {e}")
            return []
    
    def auto_reply_to_topic(self, topic_url, reply_content=None):
        """自动回复主题"""
        if not reply_content:
            reply_content = random.choice(self.config.REPLY_TEMPLATES)
        
        try:
            if not self.driver:
                if not self.init_driver() or not self.login():
                    return False
            
            # 访问主题页面
            self.driver.get(topic_url)
            time.sleep(2)
            
            # 查找快速回复框
            try:
                reply_textarea = self.driver.find_element(By.ID, "fastpostmessage")
                reply_textarea.clear()
                reply_textarea.send_keys(reply_content)
                
                # 点击快速回复按钮
                reply_button = self.driver.find_element(By.ID, "fastpostsubmit")
                reply_button.click()
                
                time.sleep(2)
                self.logger.info(f"成功回复主题: {topic_url}")
                return True
                
            except NoSuchElementException:
                self.logger.warning("未找到快速回复框，尝试其他方式")
                return False
                
        except Exception as e:
            self.logger.error(f"回复主题失败: {e}")
            return False
    
    def create_topic(self, title, content, forum_id):
        """创建新主题"""
        try:
            if not self.driver:
                if not self.init_driver() or not self.login():
                    return False
            
            # 访问发帖页面
            post_url = f"{self.config.FORUM_URL}/forum.php?mod=post&action=newthread&fid={forum_id}"
            self.driver.get(post_url)
            time.sleep(2)
            
            # 填写标题
            title_input = self.driver.find_element(By.ID, "subject")
            title_input.clear()
            title_input.send_keys(title)
            
            # 填写内容
            content_textarea = self.driver.find_element(By.ID, "e_textarea")
            content_textarea.clear()
            content_textarea.send_keys(content)
            
            # 提交帖子
            submit_button = self.driver.find_element(By.ID, "postsubmit")
            submit_button.click()
            
            time.sleep(3)
            self.logger.info(f"成功创建主题: {title}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建主题失败: {e}")
            return False
    
    def run_auto_reply(self):
        """运行自动回复任务"""
        if not self.config.AUTO_REPLY_ENABLED:
            return
        
        self.logger.info("开始自动回复任务")
        
        # 获取新主题
        topics = self.get_new_topics(limit=5)
        
        for topic in topics:
            try:
                # 随机延迟，避免过于频繁
                time.sleep(random.randint(30, 120))
                
                # 自动回复
                success = self.auto_reply_to_topic(topic['url'])
                if success:
                    self.logger.info(f"成功回复主题: {topic['title']}")
                else:
                    self.logger.warning(f"回复主题失败: {topic['title']}")
                    
            except Exception as e:
                self.logger.error(f"处理主题时出错: {e}")
                continue
    
    def run_auto_create_topic(self):
        """运行自动创建主题任务"""
        if not self.config.AUTO_CREATE_TOPIC_ENABLED:
            return
        
        self.logger.info("开始自动创建主题任务")
        
        # 随机选择一个主题模板
        template = random.choice(self.config.TOPIC_TEMPLATES)
        
        try:
            success = self.create_topic(
                template['title'],
                template['content'],
                template['forum_id']
            )
            
            if success:
                self.logger.info(f"成功创建主题: {template['title']}")
            else:
                self.logger.warning(f"创建主题失败: {template['title']}")
                
        except Exception as e:
            self.logger.error(f"创建主题时出错: {e}")
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.logger.info("浏览器已关闭")
