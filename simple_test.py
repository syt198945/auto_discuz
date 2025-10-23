"""
简化版论坛自动化测试
"""
import requests
import time
from bs4 import BeautifulSoup

def test_forum_connection():
    """测试论坛连接"""
    print("=" * 50)
    print("ZelosTech 论坛连接测试")
    print("=" * 50)
    
    forum_url = "http://bbs.zelostech.com.cn"
    username = "yurisun"
    password = "sunyuting0"
    
    print(f"论坛地址: {forum_url}")
    print(f"用户名: {username}")
    print(f"密码: {'*' * len(password)}")
    print()
    
    try:
        # 创建会话
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        print("1. 测试论坛访问...")
        response = session.get(forum_url)
        if response.status_code == 200:
            print("✅ 论坛访问成功")
        else:
            print(f"❌ 论坛访问失败，状态码: {response.status_code}")
            return False
        
        print("\n2. 获取论坛页面内容...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找登录表单
        login_form = soup.find('form', {'name': 'login'})
        if login_form:
            print("✅ 找到登录表单")
        else:
            print("⚠️  未找到登录表单，尝试其他方式")
        
        # 查找论坛标题
        title = soup.find('title')
        if title:
            print(f"✅ 论坛标题: {title.get_text().strip()}")
        
        # 查找论坛链接
        forum_links = soup.find_all('a', href=True)
        print(f"✅ 找到 {len(forum_links)} 个链接")
        
        # 显示前几个链接
        print("\n前5个链接:")
        for i, link in enumerate(forum_links[:5], 1):
            href = link.get('href')
            text = link.get_text().strip()
            if href and text:
                print(f"   {i}. {text} -> {href}")
        
        print("\n✅ 论坛连接测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

if __name__ == "__main__":
    test_forum_connection()

