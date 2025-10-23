"""
手动登录测试脚本 - 用于验证用户名和密码
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def manual_login_test():
    """手动测试登录"""
    print("手动登录测试")
    print("=" * 40)
    print("用户名: yurisun")
    print("密码: sunyuting0")
    print("=" * 40)
    
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,800')
    
    driver = None
    try:
        print("1. 启动浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        print("[OK] 浏览器启动成功")
        
        print("\n2. 访问登录页面...")
        driver.get("http://bbs.zelostech.com.cn/member.php?mod=logging&action=login")
        time.sleep(3)
        
        print(f"页面标题: {driver.title}")
        print(f"页面URL: {driver.current_url}")
        
        print("\n3. 请手动输入登录信息...")
        print("请在浏览器中手动输入:")
        print("- 用户名: yurisun")
        print("- 密码: sunyuting0")
        print("- 安全提问: 选择 '无' 或第一个选项")
        print("- 点击登录按钮")
        
        input("\n按回车键继续（完成手动登录后）...")
        
        print("\n4. 检查登录结果...")
        page_source = driver.page_source
        
        # 检查登录成功标识
        success_indicators = [
            "欢迎",
            "退出", 
            "logout",
            "个人中心",
            "我的",
            "yurisun"
        ]
        
        login_success = False
        for indicator in success_indicators:
            if indicator in page_source:
                print(f"[OK] 找到登录成功标识: {indicator}")
                login_success = True
                break
        
        if not login_success:
            print("[ERROR] 未找到登录成功标识")
            
            # 检查错误信息
            error_indicators = [
                "用户名或密码错误",
                "登录失败",
                "密码错误",
                "用户不存在",
                "验证码错误"
            ]
            
            for error in error_indicators:
                if error in page_source:
                    print(f"[ERROR] 找到错误信息: {error}")
                    break
            
            print("\n页面内容预览:")
            print(page_source[:800] + "...")
        else:
            print("[OK] 手动登录成功！")
            
        print(f"\n当前页面标题: {driver.title}")
        print(f"当前页面URL: {driver.current_url}")
        
    except Exception as e:
        print(f"[ERROR] 测试过程出错: {e}")
    finally:
        if driver:
            input("\n按回车键关闭浏览器...")
            driver.quit()

if __name__ == "__main__":
    manual_login_test()

