"""
论坛自动化主程序
"""
import argparse
import logging
from discuz_automation import DiscuzAutomation
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Discuz 论坛自动化工具')
    parser.add_argument('--mode', choices=['reply', 'create', 'both'], default='both',
                       help='运行模式: reply(仅回复), create(仅创建), both(两者都执行)')
    parser.add_argument('--once', action='store_true', help='只执行一次，不持续运行')
    
    args = parser.parse_args()
    
    # 设置日志
    config = Config()
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    # 创建自动化实例
    automation = DiscuzAutomation()
    
    try:
        logger.info("论坛自动化工具启动")
        logger.info(f"运行模式: {args.mode}")
        
        if args.mode in ['reply', 'both']:
            logger.info("开始自动回复任务")
            automation.run_auto_reply()
        
        if args.mode in ['create', 'both']:
            logger.info("开始自动创建主题任务")
            automation.run_auto_create_topic()
        
        if not args.once:
            logger.info("进入持续运行模式，按 Ctrl+C 停止")
            import time
            while True:
                time.sleep(60)
                if args.mode in ['reply', 'both']:
                    automation.run_auto_reply()
                if args.mode in ['create', 'both']:
                    automation.run_auto_create_topic()
    
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭...")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        automation.close()
        logger.info("程序已关闭")

if __name__ == "__main__":
    main()
