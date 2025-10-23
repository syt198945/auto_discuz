"""
快速启动论坛自动化
"""
import sys
import time
from discuz_automation import DiscuzAutomation
from config import Config

def show_menu():
    """显示菜单"""
    print("\n" + "=" * 50)
    print("ZelosTech 论坛自动化工具")
    print("=" * 50)
    print("1. 测试连接和登录")
    print("2. 运行自动回复（单次）")
    print("3. 创建新主题（单次）")
    print("4. 启动定时任务（持续运行）")
    print("5. 查看配置信息")
    print("0. 退出")
    print("=" * 50)

def test_connection():
    """测试连接"""
    print("\n正在测试论坛连接...")
    automation = DiscuzAutomation()
    
    try:
        if automation.init_driver() and automation.login():
            print("✅ 连接测试成功！")
            topics = automation.get_new_topics(limit=3)
            if topics:
                print(f"✅ 成功获取 {len(topics)} 个主题")
            return True
        else:
            print("❌ 连接测试失败")
            return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False
    finally:
        automation.close()

def run_auto_reply():
    """运行自动回复"""
    print("\n正在运行自动回复...")
    automation = DiscuzAutomation()
    
    try:
        automation.run_auto_reply()
        print("✅ 自动回复任务完成")
    except Exception as e:
        print(f"❌ 自动回复出错: {e}")
    finally:
        automation.close()

def create_topic():
    """创建主题"""
    print("\n正在创建新主题...")
    automation = DiscuzAutomation()
    
    try:
        automation.run_auto_create_topic()
        print("✅ 主题创建任务完成")
    except Exception as e:
        print(f"❌ 创建主题出错: {e}")
    finally:
        automation.close()

def start_scheduler():
    """启动定时任务"""
    print("\n正在启动定时任务...")
    print("按 Ctrl+C 停止定时任务")
    
    try:
        from scheduler import ForumScheduler
        scheduler = ForumScheduler()
        scheduler.run()
    except KeyboardInterrupt:
        print("\n定时任务已停止")
    except Exception as e:
        print(f"❌ 定时任务出错: {e}")

def show_config():
    """显示配置信息"""
    config = Config()
    print("\n当前配置信息:")
    print(f"论坛地址: {config.FORUM_URL}")
    print(f"论坛名称: {config.FORUM_NAME}")
    print(f"用户名: {config.USERNAME}")
    print(f"自动回复: {'开启' if config.AUTO_REPLY_ENABLED else '关闭'}")
    print(f"自动创建主题: {'开启' if config.AUTO_CREATE_TOPIC_ENABLED else '关闭'}")
    print(f"回复检查间隔: {config.REPLY_CHECK_INTERVAL}秒")
    print(f"主题创建时间: {config.TOPIC_CREATE_SCHEDULE}")

def main():
    """主函数"""
    while True:
        show_menu()
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == '0':
            print("再见！")
            break
        elif choice == '1':
            test_connection()
        elif choice == '2':
            run_auto_reply()
        elif choice == '3':
            create_topic()
        elif choice == '4':
            start_scheduler()
        elif choice == '5':
            show_config()
        else:
            print("无效选择，请重新输入")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
