"""
本地运行论坛自动化 - 替代 Background Agent
"""
import os
import sys
import time
import subprocess
import threading
from datetime import datetime
from discuz_automation import DiscuzAutomation
from scheduler import ForumScheduler
from config import Config

class LocalRunner:
    def __init__(self):
        self.config = Config()
        self.automation = None
        self.scheduler = None
        self.running = False
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        import logging
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('local_runner.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def install_dependencies(self):
        """安装依赖包"""
        print("正在安装依赖包...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("[OK] 依赖包安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] 依赖包安装失败: {e}")
            return False
    
    def test_connection(self):
        """测试连接"""
        print("\n正在测试论坛连接...")
        self.automation = DiscuzAutomation()
        
        try:
            if self.automation.init_driver() and self.automation.login():
                print("[OK] 论坛连接测试成功！")
                topics = self.automation.get_new_topics(limit=3)
                if topics:
                    print(f"[OK] 成功获取 {len(topics)} 个主题")
                    for i, topic in enumerate(topics, 1):
                        print(f"   {i}. {topic['title']}")
                return True
            else:
                print("[ERROR] 论坛连接测试失败")
                return False
        except Exception as e:
            print(f"[ERROR] 连接测试出错: {e}")
            return False
        finally:
            if self.automation:
                self.automation.close()
    
    def run_automation(self):
        """运行自动化任务"""
        self.logger.info("开始运行自动化任务")
        
        try:
            # 运行自动回复
            if self.config.AUTO_REPLY_ENABLED:
                self.logger.info("执行自动回复任务")
                self.automation = DiscuzAutomation()
                self.automation.run_auto_reply()
                self.automation.close()
            
            # 运行自动创建主题
            if self.config.AUTO_CREATE_TOPIC_ENABLED:
                self.logger.info("执行自动创建主题任务")
                self.automation = DiscuzAutomation()
                self.automation.run_auto_create_topic()
                self.automation.close()
                
        except Exception as e:
            self.logger.error(f"自动化任务执行失败: {e}")
    
    def run_scheduler(self):
        """运行定时调度器"""
        self.logger.info("启动定时调度器")
        self.running = True
        
        try:
            self.scheduler = ForumScheduler()
            self.scheduler.run()
        except KeyboardInterrupt:
            self.logger.info("收到停止信号")
        except Exception as e:
            self.logger.error(f"调度器运行出错: {e}")
        finally:
            self.running = False
    
    def show_status(self):
        """显示运行状态"""
        while self.running:
            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] 论坛自动化运行中... (按 Ctrl+C 停止)", end='', flush=True)
            time.sleep(1)
    
    def start(self):
        """启动本地运行器"""
        print("=" * 60)
        print("ZelosTech 论坛自动化 - 本地运行模式")
        print("=" * 60)
        
        # 1. 安装依赖
        if not self.install_dependencies():
            return
        
        # 2. 测试连接
        if not self.test_connection():
            print("\n[ERROR] 连接测试失败，请检查网络和账户信息")
            return
        
        # 3. 选择运行模式
        print("\n请选择运行模式:")
        print("1. 单次执行（执行一次后退出）")
        print("2. 定时运行（持续运行，按 Ctrl+C 停止）")
        print("3. 仅测试连接")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == '1':
            print("\n执行单次自动化任务...")
            self.run_automation()
            print("[OK] 任务执行完成")
            
        elif choice == '2':
            print("\n启动定时运行模式...")
            print("按 Ctrl+C 停止运行")
            
            # 在后台线程运行调度器
            scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
            scheduler_thread.start()
            
            # 在主线程显示状态
            try:
                self.running = True
                self.show_status()
            except KeyboardInterrupt:
                print("\n\n正在停止...")
                self.running = False
                
        elif choice == '3':
            print("[OK] 连接测试完成")
        else:
            print("无效选择")

def main():
    """主函数"""
    runner = LocalRunner()
    runner.start()

if __name__ == "__main__":
    main()
