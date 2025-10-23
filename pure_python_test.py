"""
纯 Python 论坛连接测试（不依赖外部包）
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import re
from html.parser import HTMLParser

class SimpleHTMLParser(HTMLParser):
    """简单的 HTML 解析器"""
    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.forms = []
        self.in_title = False
        self.in_form = False
        self.current_form = {}
        self.current_link = {}
    
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'a':
            href = dict(attrs).get('href', '')
            text = ""
            self.current_link = {'href': href, 'text': text}
        elif tag == 'form':
            self.in_form = True
            self.current_form = dict(attrs)
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'a' and self.current_link:
            self.links.append(self.current_link)
            self.current_link = {}
        elif tag == 'form':
            self.in_form = False
            if self.current_form:
                self.forms.append(self.current_form)
                self.current_form = {}
    
    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        elif self.current_link:
            self.current_link['text'] += data.strip()

def test_forum_connection():
    """测试论坛连接"""
    print("=" * 60)
    print("ZelosTech 论坛连接测试（纯 Python 版本）")
    print("=" * 60)
    
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
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
        
        print("\n2. 解析论坛页面内容...")
        parser = SimpleHTMLParser()
        parser.feed(content)
        
        # 显示解析结果
        if parser.title:
            print(f"✅ 论坛标题: {parser.title}")
        else:
            print("⚠️  未找到论坛标题")
        
        if parser.forms:
            print(f"✅ 找到 {len(parser.forms)} 个表单")
            for i, form in enumerate(parser.forms, 1):
                action = form.get('action', '无')
                method = form.get('method', 'GET')
                print(f"   表单 {i}: {method} -> {action}")
        else:
            print("⚠️  未找到表单")
        
        if parser.links:
            print(f"✅ 找到 {len(parser.links)} 个链接")
            print("\n前5个链接:")
            for i, link in enumerate(parser.links[:5], 1):
                href = link.get('href', '')
                text = link.get('text', '')[:30]  # 限制长度
                if href and text:
                    print(f"   {i}. {text} -> {href}")
        else:
            print("⚠️  未找到链接")
        
        # 检查是否包含论坛相关内容
        forum_keywords = ['论坛', 'forum', 'discuz', '登录', 'login', '注册', 'register']
        found_keywords = []
        for keyword in forum_keywords:
            if keyword.lower() in content.lower():
                found_keywords.append(keyword)
        
        if found_keywords:
            print(f"✅ 检测到论坛关键词: {', '.join(found_keywords)}")
        else:
            print("⚠️  未检测到明显的论坛关键词")
        
        print("\n✅ 论坛连接测试完成！")
        print("\n📋 测试总结:")
        print(f"   - 连接状态: 成功")
        print(f"   - 页面标题: {parser.title or '未找到'}")
        print(f"   - 表单数量: {len(parser.forms)}")
        print(f"   - 链接数量: {len(parser.links)}")
        print(f"   - 关键词匹配: {len(found_keywords)} 个")
        
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ 网络连接错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "=" * 60)
    print("🎯 后续步骤建议")
    print("=" * 60)
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
        print("\n❌ 连接测试失败，请检查网络和论坛地址")
