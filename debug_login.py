"""
调试登录问题的脚本
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config

def debug_login():
    """调试登录过程"""
    print("=" * 60)
    print("Discuz 论坛登录调试工具")
    print("=" * 60)
    
    config = Config()
    print(f"论坛地址: {config.FORUM_URL}")
    print(f"用户名: {config.USERNAME}")
    print(f"密码: {'*' * len(config.PASSWORD)}")
    print()
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    # 暂时不使用无头模式，方便调试
    # chrome_options.add_argument('--headless')
    
    driver = None
    try:
        print("1. 初始化浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ 浏览器初始化成功")
        
        print("\n2. 访问论坛首页...")
        driver.get(config.FORUM_URL)
        time.sleep(3)
        
        print(f"当前页面标题: {driver.title}")
        print(f"当前页面URL: {driver.current_url}")
        
        # 检查页面是否包含论坛相关内容
        page_source = driver.page_source
        if "论坛" in page_source or "discuz" in page_source.lower():
            print("✅ 页面包含论坛相关内容")
        else:
            print("❌ 页面可能不是论坛页面")
            print("页面内容预览:")
            print(page_source[:500] + "...")
        
        print("\n3. 查找登录链接...")
        login_links = []
        try:
            # 尝试多种可能的登录链接选择器
            selectors = [
                "a[href*='logging']",
                "a[href*='login']", 
                "a:contains('登录')",
                "a:contains('Login')",
                ".login",
                "#login"
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        if elem.get_attribute('href'):
                            login_links.append(elem.get_attribute('href'))
                            print(f"找到登录链接: {elem.get_attribute('href')}")
                except:
                    continue
            
            if not login_links:
                print("❌ 未找到登录链接，尝试直接访问登录页面...")
                login_url = f"{config.FORUM_URL}/member.php?mod=logging&action=login"
            else:
                login_url = login_links[0]
                
        except Exception as e:
            print(f"查找登录链接时出错: {e}")
            login_url = f"{config.FORUM_URL}/member.php?mod=logging&action=login"
        
        print(f"\n4. 访问登录页面: {login_url}")
        driver.get(login_url)
        time.sleep(3)
        
        print(f"登录页面标题: {driver.title}")
        print(f"登录页面URL: {driver.current_url}")
        
        print("\n5. 查找登录表单元素...")
        try:
            wait = WebDriverWait(driver, 10)
            
            # 尝试多种可能的用户名输入框选择器
            username_selectors = [
                "input[name='username']",
                "input[name='login_username']", 
                "input[id='username']",
                "input[id='login_username']",
                "input[type='text']"
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    username_input = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到用户名输入框: {selector}")
                    break
                except:
                    continue
            
            if not username_input:
                print("❌ 未找到用户名输入框")
                print("页面表单元素:")
                inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    print(f"  - {inp.get_attribute('outerHTML')}")
                return False
            
            # 尝试多种可能的密码输入框选择器
            password_selectors = [
                "input[name='password']",
                "input[name='login_password']",
                "input[id='password']", 
                "input[id='login_password']",
                "input[type='password']"
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到密码输入框: {selector}")
                    break
                except:
                    continue
            
            if not password_input:
                print("❌ 未找到密码输入框")
                return False
            
            print("\n6. 填写登录信息...")
            username_input.clear()
            username_input.send_keys(config.USERNAME)
            password_input.clear()
            password_input.send_keys(config.PASSWORD)
            
            print("✅ 登录信息填写完成")
            
            print("\n7. 查找登录按钮...")
            # 尝试多种可能的登录按钮选择器
            button_selectors = [
                "input[name='loginsubmit']",
                "button[name='loginsubmit']",
                "input[type='submit']",
                "button[type='submit']",
                ".login-btn",
                "#login-btn"
            ]
            
            login_button = None
            for selector in button_selectors:
                try:
                    login_button = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ 找到登录按钮: {selector}")
                    break
                except:
                    continue
            
            if not login_button:
                print("❌ 未找到登录按钮")
                return False
            
            print("\n8. 点击登录按钮...")
            login_button.click()
            time.sleep(5)  # 等待登录处理
            
            print(f"登录后页面标题: {driver.title}")
            print(f"登录后页面URL: {driver.current_url}")
            
            print("\n9. 检查登录结果...")
            page_source = driver.page_source
            
            # 检查多种登录成功的标识
            success_indicators = [
                "欢迎",
                "退出", 
                "logout",
                "个人中心",
                "我的",
                config.USERNAME
            ]
            
            login_success = False
            for indicator in success_indicators:
                if indicator in page_source:
                    print(f"✅ 找到登录成功标识: {indicator}")
                    login_success = True
                    break
            
            if not login_success:
                print("❌ 未找到登录成功标识")
                
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
                        print(f"❌ 找到错误信息: {error}")
                        break
                
                print("\n页面内容预览:")
                print(page_source[:1000] + "...")
                return False
            else:
                print("✅ 登录成功！")
                return True
                
        except Exception as e:
            print(f"❌ 登录过程出错: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 调试过程出错: {e}")
        return False
    finally:
        if driver:
            print("\n关闭浏览器...")
            time.sleep(2)  # 等待用户查看结果
            driver.quit()

if __name__ == "__main__":
    debug_login()
    input("\n按回车键退出...")

