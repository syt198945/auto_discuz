"""
简化版论坛连接测试
"""
import urllib.request
import urllib.error
import re

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
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        print("1. 测试论坛访问...")
        req = urllib.request.Request(forum_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("[成功] 论坛访问成功")
                content = response.read().decode('utf-8', errors='ignore')
            else:
                print(f"[失败] 论坛访问失败，状态码: {response.status}")
                return False
        
        print("\n2. 分析页面内容...")
        
        # 查找标题
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            print(f"[成功] 论坛标题: {title}")
        else:
            print("[警告] 未找到论坛标题")
        
        # 查找表单
        forms = re.findall(r'<form[^>]*>', content, re.IGNORECASE)
        if forms:
            print(f"[成功] 找到 {len(forms)} 个表单")
        else:
            print("[警告] 未找到表单")
        
        # 查找链接
        links = re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>([^<]*)</a>', content, re.IGNORECASE)
        if links:
            print(f"[成功] 找到 {len(links)} 个链接")
            print("\n前5个链接:")
            for i, (href, text) in enumerate(links[:5], 1):
                text = text.strip()[:30]
                if href and text:
                    print(f"   {i}. {text} -> {href}")
        else:
            print("[警告] 未找到链接")
        
        # 检查论坛关键词
        forum_keywords = ['论坛', 'forum', 'discuz', '登录', 'login', '注册', 'register']
        found_keywords = []
        for keyword in forum_keywords:
            if keyword.lower() in content.lower():
                found_keywords.append(keyword)
        
        if found_keywords:
            print(f"[成功] 检测到论坛关键词: {', '.join(found_keywords)}")
        else:
            print("[警告] 未检测到明显的论坛关键词")
        
        print("\n[成功] 论坛连接测试完成！")
        print("\n测试总结:")
        print(f"   - 连接状态: 成功")
        print(f"   - 页面标题: {title_match.group(1).strip() if title_match else '未找到'}")
        print(f"   - 表单数量: {len(forms)}")
        print(f"   - 链接数量: {len(links)}")
        print(f"   - 关键词匹配: {len(found_keywords)} 个")
        
        return True
        
    except urllib.error.URLError as e:
        print(f"[错误] 网络连接错误: {e}")
        return False
    except Exception as e:
        print(f"[错误] 测试过程中出错: {e}")
        return False

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "=" * 50)
    print("后续步骤建议")
    print("=" * 50)
    print("1. 如果连接测试成功，可以继续安装完整版依赖:")
    print("   pip install selenium schedule fake-useragent")
    print()
    print("2. 运行完整版自动化工具:")
    print("   python run_local.py")
    print()
    print("3. 或者使用批处理文件:")
    print("   双击 start_forum_automation.bat")
    print()
    print("4. 查看详细使用指南:")
    print("   打开 使用指南.md 文件")

if __name__ == "__main__":
    success = test_forum_connection()
    if success:
        show_next_steps()
    else:
        print("\n[失败] 连接测试失败，请检查网络和论坛地址")

