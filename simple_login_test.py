"""
简单的登录测试脚本
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def simple_login_test():
    """简单登录测试"""
    print("简单登录测试")
    print("=" * 30)
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,800')
    # 暂时不使用无头模式，方便观察
    
    driver = None
    try:
        print("启动浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        print("[OK] 浏览器启动成功")
        
        print("\n访问登录页面...")
        driver.get("http://bbs.zelostech.com.cn/member.php?mod=logging&action=login")
        time.sleep(3)
        
        print(f"页面标题: {driver.title}")
        
        print("\n填写登录信息...")
        wait = WebDriverWait(driver, 10)
        
        # 输入用户名
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.clear()
        username_input.send_keys("yurisun")
        print("输入用户名: yurisun")
        
        # 输入密码
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys("sunyuting0")
        print("输入密码: sunyuting0")
        
        # 处理安全提问
        try:
            security_element = driver.find_element(By.NAME, "questionid")
            select = Select(security_element)
            if len(select.options) > 0:
                select.select_by_index(0)
                print("设置安全提问: 无")
        except:
            print("未找到安全提问字段")
        
        print("\n点击登录按钮...")
        login_button = driver.find_element(By.NAME, "loginsubmit")
        login_button.click()
        
        # 等待登录处理
        print("等待登录处理...")
        time.sleep(5)
        
        print(f"登录后页面标题: {driver.title}")
        print(f"登录后页面URL: {driver.current_url}")
        
        # 检查登录结果
        page_source = driver.page_source
        
        success_indicators = ["欢迎", "退出", "logout", "个人中心", "我的", "yurisun"]
        login_success = False
        
        for indicator in success_indicators:
            if indicator in page_source:
                print(f"[OK] 找到登录成功标识: {indicator}")
                login_success = True
                break
        
        if not login_success:
            print("[ERROR] 登录失败")
            
            # 检查错误信息
            error_indicators = ["用户名或密码错误", "登录失败", "密码错误", "用户不存在", "验证码错误"]
            for error in error_indicators:
                if error in page_source:
                    print(f"[ERROR] 错误信息: {error}")
                    break
            
            # 保存页面源码用于分析
            with open("login_result.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            print("页面源码已保存到 login_result.html")
        else:
            print("[OK] 登录成功！")
            
        # 等待用户查看结果
        print("\n等待10秒后关闭浏览器...")
        time.sleep(10)
        
    except Exception as e:
        print(f"[ERROR] 测试过程出错: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    simple_login_test()

