#!/usr/bin/env python3
"""
GitHub Actions 快速设置脚本
帮助用户快速配置GitHub Actions环境
"""
import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    """打印横幅"""
    print("=" * 60)
    print("🚀 GitHub Actions 快速设置")
    print("=" * 60)
    print()

def check_git_repo():
    """检查是否为Git仓库"""
    if not os.path.exists('.git'):
        print("❌ 当前目录不是Git仓库")
        print("请先初始化Git仓库：")
        print("  git init")
        print("  git remote add origin <your-repo-url>")
        return False
    return True

def check_github_remote():
    """检查GitHub远程仓库"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'github.com' not in result.stdout:
            print("❌ 未找到GitHub远程仓库")
            print("请添加GitHub远程仓库：")
            print("  git remote add origin https://github.com/username/repo.git")
            return False
        return True
    except:
        return False

def create_github_secrets_guide():
    """创建GitHub Secrets配置指南"""
    guide = """
# GitHub Secrets 配置指南

## 步骤1：访问仓库设置
1. 打开您的GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Secrets and variables" -> "Actions"

## 步骤2：添加Secrets
点击 "New repository secret" 添加以下secrets：

### FORUM_USERNAME
- Name: FORUM_USERNAME
- Value: 您的论坛用户名（例如：yurisun）

### FORUM_PASSWORD  
- Name: FORUM_PASSWORD
- Value: 您的论坛密码

## 步骤3：验证配置
添加完成后，您应该看到两个secrets：
- FORUM_USERNAME
- FORUM_PASSWORD

## 注意事项
- Secrets是加密存储的，只有您和GitHub Actions可以访问
- 不要在代码中硬编码密码
- 定期更新密码以确保安全
"""
    
    with open('GITHUB_SECRETS_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("📝 已创建 GitHub Secrets 配置指南：GITHUB_SECRETS_GUIDE.md")

def check_workflow_files():
    """检查工作流文件"""
    workflow_dir = Path('.github/workflows')
    if not workflow_dir.exists():
        print("❌ 工作流目录不存在")
        return False
    
    required_files = ['timed-reply.yml', 'continuous-reply.yml']
    missing_files = []
    
    for file in required_files:
        if not (workflow_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少工作流文件：{', '.join(missing_files)}")
        return False
    
    print("✅ 工作流文件检查通过")
    return True

def check_python_files():
    """检查Python文件"""
    required_files = ['github_runner.py', 'config.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少Python文件：{', '.join(missing_files)}")
        return False
    
    print("✅ Python文件检查通过")
    return True

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "=" * 60)
    print("🎯 后续步骤")
    print("=" * 60)
    print()
    print("1. 配置GitHub Secrets：")
    print("   - 按照 GITHUB_SECRETS_GUIDE.md 的说明配置")
    print("   - 添加 FORUM_USERNAME 和 FORUM_PASSWORD")
    print()
    print("2. 推送代码到GitHub：")
    print("   git add .")
    print("   git commit -m 'Add GitHub Actions workflows'")
    print("   git push origin main")
    print()
    print("3. 启用工作流：")
    print("   - 访问GitHub仓库的Actions页面")
    print("   - 选择 'Timed Reply Bot' 或 'Continuous Reply Bot'")
    print("   - 点击 'Run workflow' 开始运行")
    print()
    print("4. 监控运行状态：")
    print("   - 在Actions页面查看运行日志")
    print("   - 下载日志文件查看详细信息")
    print()
    print("🎉 设置完成！您的定时回复机器人将在GitHub后台运行")

def main():
    """主函数"""
    print_banner()
    
    # 检查Git仓库
    if not check_git_repo():
        return
    
    # 检查GitHub远程仓库
    if not check_github_remote():
        return
    
    # 检查工作流文件
    if not check_workflow_files():
        return
    
    # 检查Python文件
    if not check_python_files():
        return
    
    # 创建配置指南
    create_github_secrets_guide()
    
    # 显示后续步骤
    show_next_steps()

if __name__ == "__main__":
    main()
