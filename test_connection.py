"""
测试论坛连接和登录功能
"""
import time
from discuz_automation import DiscuzAutomation
from config import Config

def test_forum_connection():
    """测试论坛连接"""
    print("=" * 50)
    print("ZelosTech 论坛自动化测试")
    print("=" * 50)
    
    config = Config()
    print(f"论坛地址: {config.FORUM_URL}")
    print(f"用户名: {config.USERNAME}")
    print(f"密码: {'*' * len(config.PASSWORD)}")
    print()
    
    automation = DiscuzAutomation()
    
    try:
        print("1. 初始化浏览器驱动...")
        if not automation.init_driver():
            print("[ERROR] 浏览器驱动初始化失败")
            return False
        print("[OK] 浏览器驱动初始化成功")
        
        print("\n2. 测试论坛访问...")
        automation.driver.get(config.FORUM_URL)
        time.sleep(3)
        
        if "ZelosTech" in automation.driver.page_source or "论坛" in automation.driver.page_source:
            print("[OK] 论坛访问成功")
        else:
            print("[ERROR] 论坛访问失败")
            return False
        
        print("\n3. 测试登录功能...")
        if automation.login():
            print("[OK] 登录成功")
            
            print("\n4. 测试获取主题列表...")
            topics = automation.get_new_topics(limit=3)
            if topics:
                print(f"[OK] 成功获取 {len(topics)} 个主题")
                for i, topic in enumerate(topics, 1):
                    print(f"   {i}. {topic['title']}")
            else:
                print("[WARNING] 未获取到主题，可能是论坛结构需要调整")
            
            print("\n5. 测试完成，所有功能正常！")
            return True
        else:
            print("[ERROR] 登录失败，请检查用户名密码")
            return False
            
    except Exception as e:
        print(f"[ERROR] 测试过程中出错: {e}")
        return False
    finally:
        automation.close()
        print("\n浏览器已关闭")

if __name__ == "__main__":
    test_forum_connection()
