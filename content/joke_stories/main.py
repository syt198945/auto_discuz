#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笑话故事主程序
提供命令行接口和API接口
"""

import argparse
import json
import sys
import os
from typing import Dict, Any
import logging
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from joke_search import JokeSearcher
from joke_generator import JokeGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JokeStoriesApp:
    """笑话故事应用程序"""
    
    def __init__(self):
        self.searcher = JokeSearcher()
        self.generator = JokeGenerator()
    
    def run_cli(self, args):
        """运行命令行界面"""
        try:
            if args.command == 'search':
                self._handle_search_command(args)
            elif args.command == 'generate':
                self._handle_generate_command(args)
            elif args.command == 'collection':
                self._handle_collection_command(args)
            elif args.command == 'random':
                self._handle_random_command(args)
            elif args.command == 'forum':
                self._handle_forum_command(args)
            elif args.command == 'social':
                self._handle_social_command(args)
            elif args.command == 'email':
                self._handle_email_command(args)
            elif args.command == 'save':
                self._handle_save_command(args)
            else:
                print("未知命令，请使用 --help 查看帮助信息")
                
        except Exception as e:
            logger.error(f"执行命令时发生错误: {e}")
            print(f"错误: {e}")
    
    def _handle_search_command(self, args):
        """处理搜索命令"""
        print(f"正在搜索 {args.count} 个 {args.category} 笑话...")
        
        if args.category == 'programming':
            jokes = self.searcher.search_programming_jokes(args.count)
        elif args.category == 'dad':
            jokes = self.searcher.search_dad_jokes(args.count)
        else:
            jokes = self.searcher.search_jokes(args.count, args.category)
        
        if not jokes:
            print("没有找到笑话")
            return
        
        for i, joke in enumerate(jokes, 1):
            print(f"\n{i}. {joke['title']}")
            print(f"   {joke['content']}")
            print(f"   来源: {joke['source']}")
    
    def _handle_generate_command(self, args):
        """处理生成命令"""
        print(f"正在生成 {args.count} 个 {args.category} 笑话...")
        
        text = self.generator.generate_joke_text(
            count=args.count,
            format_type=args.format,
            category=args.category,
            include_metadata=args.metadata
        )
        
        print("\n" + "="*50)
        print(text)
        print("="*50)
    
    def _handle_collection_command(self, args):
        """处理合集命令"""
        categories = args.categories.split(',') if args.categories else ['any', 'programming', 'dad']
        
        print(f"正在生成笑话合集，包含类别: {', '.join(categories)}")
        
        text = self.generator.generate_joke_collection(
            categories=categories,
            jokes_per_category=args.per_category,
            format_type=args.format
        )
        
        print("\n" + "="*50)
        print(text)
        print("="*50)
    
    def _handle_random_command(self, args):
        """处理随机笑话命令"""
        print("正在生成随机笑话...")
        
        text = self.generator.generate_random_joke(args.format)
        
        print("\n" + "="*50)
        print(text)
        print("="*50)
    
    def _handle_forum_command(self, args):
        """处理论坛帖子命令"""
        print(f"正在生成 {args.category} 论坛帖子...")
        
        text = self.generator.generate_joke_for_forum(args.category)
        
        print("\n" + "="*50)
        print(text)
        print("="*50)
    
    def _handle_social_command(self, args):
        """处理社交媒体命令"""
        print(f"正在生成 {args.category} 社交媒体内容...")
        
        text = self.generator.generate_joke_for_social_media(args.category)
        
        print("\n" + "="*50)
        print(text)
        print("="*50)
    
    def _handle_email_command(self, args):
        """处理邮件命令"""
        print(f"正在生成 {args.category} 邮件...")
        
        email = self.generator.generate_joke_email(args.category)
        
        print("\n" + "="*50)
        print(f"主题: {email['subject']}")
        print(f"内容:\n{email['body']}")
        print("="*50)
    
    def _handle_save_command(self, args):
        """处理保存命令"""
        print(f"正在保存 {args.count} 个 {args.category} 笑话到 {args.filename}...")
        
        filename = self.generator.save_jokes_to_file(
            filename=args.filename,
            count=args.count,
            category=args.category,
            format_type=args.format
        )
        
        print(f"笑话已保存到: {filename}")
    
    def get_api_info(self) -> Dict[str, Any]:
        """获取API信息"""
        return {
            'available_formats': self.generator.get_available_formats(),
            'available_categories': self.generator.get_available_categories(),
            'version': '1.0.0',
            'description': '笑话故事生成器API'
        }

def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='笑话故事生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py search --count 5 --category programming
  python main.py generate --count 3 --format full_format
  python main.py random --format story_format
  python main.py forum --category dad
  python main.py social --category programming
  python main.py email --category any
  python main.py collection --categories programming,dad --per-category 2
  python main.py save --filename jokes.md --count 10 --category any
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 搜索命令
    search_parser = subparsers.add_parser('search', help='搜索笑话')
    search_parser.add_argument('--count', type=int, default=5, help='笑话数量')
    search_parser.add_argument('--category', choices=['any', 'programming', 'dad'], 
                              default='any', help='笑话类别')
    
    # 生成命令
    generate_parser = subparsers.add_parser('generate', help='生成笑话文本')
    generate_parser.add_argument('--count', type=int, default=1, help='笑话数量')
    generate_parser.add_argument('--category', choices=['any', 'programming', 'dad'], 
                                default='any', help='笑话类别')
    generate_parser.add_argument('--format', default='simple', help='文本格式')
    generate_parser.add_argument('--metadata', action='store_true', help='包含元数据')
    
    # 合集命令
    collection_parser = subparsers.add_parser('collection', help='生成笑话合集')
    collection_parser.add_argument('--categories', help='笑话类别，用逗号分隔')
    collection_parser.add_argument('--per-category', type=int, default=2, help='每个类别的笑话数量')
    collection_parser.add_argument('--format', default='full_format', help='文本格式')
    
    # 随机笑话命令
    random_parser = subparsers.add_parser('random', help='生成随机笑话')
    random_parser.add_argument('--format', default='story_format', help='文本格式')
    
    # 论坛帖子命令
    forum_parser = subparsers.add_parser('forum', help='生成论坛帖子')
    forum_parser.add_argument('--category', choices=['any', 'programming', 'dad'], 
                             default='any', help='笑话类别')
    
    # 社交媒体命令
    social_parser = subparsers.add_parser('social', help='生成社交媒体内容')
    social_parser.add_argument('--category', choices=['any', 'programming', 'dad'], 
                              default='any', help='笑话类别')
    
    # 邮件命令
    email_parser = subparsers.add_parser('email', help='生成邮件')
    email_parser.add_argument('--category', choices=['any', 'programming', 'dad'], 
                             default='any', help='笑话类别')
    
    # 保存命令
    save_parser = subparsers.add_parser('save', help='保存笑话到文件')
    save_parser.add_argument('--filename', required=True, help='文件名')
    save_parser.add_argument('--count', type=int, default=10, help='笑话数量')
    save_parser.add_argument('--category', choices=['any', 'programming', 'dad'], 
                            default='any', help='笑话类别')
    save_parser.add_argument('--format', default='markdown', help='文本格式')
    
    return parser

def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    app = JokeStoriesApp()
    app.run_cli(args)

if __name__ == "__main__":
    main()
