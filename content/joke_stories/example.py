#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笑话故事模块使用示例
"""

from joke_search import JokeSearcher
from joke_generator import JokeGenerator

def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建搜索器和生成器
    searcher = JokeSearcher()
    generator = JokeGenerator()
    
    # 搜索笑话
    print("1. 搜索编程笑话:")
    jokes = searcher.search_programming_jokes(3)
    for i, joke in enumerate(jokes, 1):
        print(f"   {i}. {joke['content']}")
    
    print("\n2. 生成格式化文本:")
    text = generator.generate_joke_text(
        count=2, 
        format_type='full_format', 
        category='programming'
    )
    print(text)

def example_advanced_usage():
    """高级使用示例"""
    print("\n=== 高级使用示例 ===")
    
    generator = JokeGenerator()
    
    # 生成笑话合集
    print("1. 生成笑话合集:")
    collection = generator.generate_joke_collection(
        categories=['programming', 'dad'],
        jokes_per_category=2,
        format_type='markdown'
    )
    print(collection)
    
    # 生成论坛帖子
    print("\n2. 生成论坛帖子:")
    forum_post = generator.generate_joke_for_forum('programming')
    print(forum_post)
    
    # 生成社交媒体内容
    print("\n3. 生成社交媒体内容:")
    social_media = generator.generate_joke_for_social_media('dad')
    print(social_media)
    
    # 生成邮件
    print("\n4. 生成邮件:")
    email = generator.generate_joke_email('any')
    print(f"主题: {email['subject']}")
    print(f"内容: {email['body']}")

def example_save_to_file():
    """保存到文件示例"""
    print("\n=== 保存到文件示例 ===")
    
    generator = JokeGenerator()
    
    # 保存编程笑话到文件
    filename = generator.save_jokes_to_file(
        filename='programming_jokes.md',
        count=5,
        category='programming',
        format_type='markdown'
    )
    print(f"编程笑话已保存到: {filename}")
    
    # 保存爸爸笑话到文件
    filename = generator.save_jokes_to_file(
        filename='dad_jokes.txt',
        count=3,
        category='dad',
        format_type='simple'
    )
    print(f"爸爸笑话已保存到: {filename}")

def example_api_info():
    """API信息示例"""
    print("\n=== API信息示例 ===")
    
    generator = JokeGenerator()
    
    print("可用格式:")
    for format_type in generator.get_available_formats():
        print(f"  - {format_type}")
    
    print("\n可用类别:")
    for category in generator.get_available_categories():
        print(f"  - {category}")

def main():
    """主函数"""
    print("笑话故事模块使用示例")
    print("="*50)
    
    try:
        example_basic_usage()
        example_advanced_usage()
        example_save_to_file()
        example_api_info()
        
        print("\n示例运行完成！")
        
    except Exception as e:
        print(f"运行示例时发生错误: {e}")

if __name__ == "__main__":
    main()
