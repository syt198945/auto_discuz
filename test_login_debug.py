"""
简单的登录调试测试脚本
"""
import os
import sys
from debug_login import debug_login

def main():
    print("Discuz 论坛登录问题调试工具")
    print("=" * 50)
    
    # 检查配置文件
    if not os.path.exists('config.py'):
        print("❌ 未找到 config.py 文件")
        return
    
    # 运行调试
    print("开始调试登录过程...")
    print("注意：此脚本会打开浏览器窗口，请观察登录过程")
    print()
    
    success = debug_login()
    
    if success:
        print("\n✅ 登录调试成功！")
        print("问题可能已解决，请重新运行论坛自动化工具")
    else:
        print("\n❌ 登录调试失败")
        print("请检查以下可能的问题：")
        print("1. 网络连接是否正常")
        print("2. 论坛地址是否正确")
        print("3. 用户名和密码是否正确")
        print("4. 是否需要验证码")
        print("5. 论坛是否正常访问")

if __name__ == "__main__":
    main()

