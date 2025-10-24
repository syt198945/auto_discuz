"""
多账户定时回复机器人主程序
"""
import argparse
import logging
import os
import sys
from timed_reply import TimedReplyBot, ConfigManager

def main():
    parser = argparse.ArgumentParser(description='多账户定时回复机器人')
    parser.add_argument('--config', default='config.json', help='配置文件路径 (默认: config.json)')
    parser.add_argument('--once', action='store_true', help='只执行一次，不持续运行')
    
    args = parser.parse_args()
    
    # 检查配置文件是否存在
    if not os.path.exists(args.config):
        print(f"错误: 配置文件 {args.config} 不存在")
        print(f"请复制 config_example.json 为 {args.config} 并修改配置")
        sys.exit(1)
    
    try:
        # 创建配置管理器
        config_manager = ConfigManager(args.config)
        
        # 创建定时回复机器人
        bot = TimedReplyBot(config_manager)
        
        print("🤖 多账户定时回复机器人启动")
        print(f"📁 配置文件: {args.config}")
        
        # 显示配置信息
        enabled_accounts = config_manager.get_enabled_accounts()
        print(f"👥 启用的账户数: {len(enabled_accounts)}")
        
        total_targets = 0
        for account in enabled_accounts:
            targets = config_manager.get_enabled_targets(account)
            total_targets += len(targets)
            print(f"  - {account['username']}: {len(targets)} 个回复目标")
        
        print(f"🎯 总回复目标数: {total_targets}")
        print("按 Ctrl+C 停止机器人")
        print("=" * 50)
        
        # 运行定时回复任务
        bot.run_timed_reply()
    
    except KeyboardInterrupt:
        print("\n🤖 收到停止信号，正在关闭...")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        logging.error(f"程序运行出错: {e}")
    finally:
        print("🤖 程序已关闭")

if __name__ == "__main__":
    main()
