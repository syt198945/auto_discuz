"""
定时任务调度器
"""
import schedule
import time
import logging
from datetime import datetime
from discuz_automation import DiscuzAutomation
from config import Config

class ForumScheduler:
    def __init__(self):
        self.config = Config()
        self.automation = DiscuzAutomation()
        self.setup_logging()
        self.setup_schedule()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_schedule(self):
        """设置定时任务"""
        # 自动回复任务 - 每5分钟检查一次
        schedule.every(self.config.REPLY_CHECK_INTERVAL).seconds.do(self.run_auto_reply)
        
        # 自动创建主题任务 - 根据配置的时间点
        schedule_times = self.config.TOPIC_CREATE_SCHEDULE.split(',')
        for schedule_time in schedule_times:
            schedule.every().day.at(schedule_time.strip()).do(self.run_auto_create_topic)
        
        self.logger.info("定时任务设置完成")
        self.logger.info(f"自动回复检查间隔: {self.config.REPLY_CHECK_INTERVAL}秒")
        self.logger.info(f"自动创建主题时间: {self.config.TOPIC_CREATE_SCHEDULE}")
    
    def run_auto_reply(self):
        """执行自动回复任务"""
        try:
            self.logger.info("执行自动回复任务")
            self.automation.run_auto_reply()
        except Exception as e:
            self.logger.error(f"自动回复任务执行失败: {e}")
    
    def run_auto_create_topic(self):
        """执行自动创建主题任务"""
        try:
            self.logger.info("执行自动创建主题任务")
            self.automation.run_auto_create_topic()
        except Exception as e:
            self.logger.error(f"自动创建主题任务执行失败: {e}")
    
    def run(self):
        """运行调度器"""
        self.logger.info("论坛自动化调度器启动")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            self.logger.info("收到停止信号，正在关闭调度器...")
        except Exception as e:
            self.logger.error(f"调度器运行出错: {e}")
        finally:
            self.automation.close()
            self.logger.info("调度器已关闭")

if __name__ == "__main__":
    scheduler = ForumScheduler()
    scheduler.run()
