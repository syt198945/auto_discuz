#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笑话文本生成接口
提供各种格式的笑话文本生成功能
"""

import json
import random
from typing import List, Dict, Optional
from datetime import datetime
import logging
from joke_search import JokeSearcher

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JokeGenerator:
    """笑话文本生成器"""
    
    def __init__(self):
        self.searcher = JokeSearcher()
        
        # 文本模板
        self.templates = {
            'simple': "{content}",
            'with_title': "{title}\n\n{content}",
            'with_source': "{content}\n\n—— 来源：{source}",
            'full_format': "{title}\n\n{content}\n\n—— 来源：{source}",
            'story_format': "今天给大家分享一个笑话：\n\n{content}\n\n希望大家喜欢！",
            'forum_post': "【笑话分享】{title}\n\n{content}\n\n#笑话 #分享",
            'social_media': "😄 今日笑话：\n\n{content}\n\n#笑话 #开心",
            'email_format': "主题：{title}\n\n内容：\n{content}\n\n祝您开心！",
            'markdown': "## {title}\n\n{content}\n\n*来源：{source}*"
        }
    
    def generate_joke_text(self, 
                          count: int = 1, 
                          format_type: str = 'simple',
                          category: str = 'any',
                          include_metadata: bool = False) -> str:
        """
        生成笑话文本
        
        Args:
            count: 生成的笑话数量
            format_type: 文本格式类型
            category: 笑话类别
            include_metadata: 是否包含元数据
            
        Returns:
            格式化的笑话文本
        """
        # 根据类别获取笑话
        if category == 'programming':
            jokes = self.searcher.search_programming_jokes(count)
        elif category == 'dad':
            jokes = self.searcher.search_dad_jokes(count)
        else:
            jokes = self.searcher.search_jokes(count, category)
        
        if not jokes:
            return "抱歉，暂时没有找到合适的笑话。"
        
        # 生成文本
        if count == 1:
            return self._format_single_joke(jokes[0], format_type, include_metadata)
        else:
            return self._format_multiple_jokes(jokes, format_type, include_metadata)
    
    def _format_single_joke(self, joke: Dict, format_type: str, include_metadata: bool) -> str:
        """格式化单个笑话"""
        template = self.templates.get(format_type, self.templates['simple'])
        
        # 准备格式化数据
        format_data = {
            'title': joke.get('title', '笑话'),
            'content': joke.get('content', ''),
            'source': joke.get('source', '未知')
        }
        
        # 添加元数据
        if include_metadata:
            format_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            format_data['category'] = joke.get('category', 'general')
        
        # 格式化文本
        try:
            formatted_text = template.format(**format_data)
        except KeyError as e:
            logger.warning(f"模板格式化失败，缺少字段: {e}")
            formatted_text = joke.get('content', '')
        
        return formatted_text
    
    def _format_multiple_jokes(self, jokes: List[Dict], format_type: str, include_metadata: bool) -> str:
        """格式化多个笑话"""
        formatted_jokes = []
        
        for i, joke in enumerate(jokes, 1):
            # 为多个笑话添加编号
            joke_copy = joke.copy()
            joke_copy['title'] = f"{joke_copy.get('title', '笑话')} ({i})"
            
            formatted_joke = self._format_single_joke(joke_copy, format_type, include_metadata)
            formatted_jokes.append(formatted_joke)
        
        # 用分隔符连接多个笑话
        separator = "\n\n" + "="*50 + "\n\n"
        return separator.join(formatted_jokes)
    
    def generate_joke_collection(self, 
                                categories: List[str] = None,
                                jokes_per_category: int = 2,
                                format_type: str = 'full_format') -> str:
        """
        生成笑话合集
        
        Args:
            categories: 笑话类别列表
            jokes_per_category: 每个类别的笑话数量
            format_type: 文本格式类型
            
        Returns:
            格式化的笑话合集文本
        """
        if categories is None:
            categories = ['any', 'programming', 'dad']
        
        collection_parts = []
        collection_parts.append("🎭 笑话合集\n")
        collection_parts.append("="*50 + "\n")
        
        for category in categories:
            # 添加类别标题
            category_title = self._get_category_title(category)
            collection_parts.append(f"\n## {category_title}\n")
            
            # 生成该类别的笑话
            jokes = self._get_jokes_by_category(category, jokes_per_category)
            
            for i, joke in enumerate(jokes, 1):
                joke_text = self._format_single_joke(joke, format_type, False)
                collection_parts.append(f"{i}. {joke_text}\n")
        
        return "\n".join(collection_parts)
    
    def _get_category_title(self, category: str) -> str:
        """获取类别标题"""
        titles = {
            'any': '综合笑话',
            'programming': '编程笑话',
            'dad': '爸爸笑话',
            'general': '一般笑话'
        }
        return titles.get(category, category.title())
    
    def _get_jokes_by_category(self, category: str, count: int) -> List[Dict]:
        """根据类别获取笑话"""
        if category == 'programming':
            return self.searcher.search_programming_jokes(count)
        elif category == 'dad':
            return self.searcher.search_dad_jokes(count)
        else:
            return self.searcher.search_jokes(count, category)
    
    def generate_random_joke(self, format_type: str = 'story_format') -> str:
        """生成随机笑话"""
        categories = ['any', 'programming', 'dad']
        category = random.choice(categories)
        
        return self.generate_joke_text(
            count=1,
            format_type=format_type,
            category=category,
            include_metadata=True
        )
    
    def generate_joke_for_forum(self, category: str = 'any') -> str:
        """生成适合论坛的笑话帖子"""
        return self.generate_joke_text(
            count=1,
            format_type='forum_post',
            category=category,
            include_metadata=False
        )
    
    def generate_joke_for_social_media(self, category: str = 'any') -> str:
        """生成适合社交媒体的笑话"""
        return self.generate_joke_text(
            count=1,
            format_type='social_media',
            category=category,
            include_metadata=False
        )
    
    def generate_joke_email(self, category: str = 'any') -> Dict[str, str]:
        """生成笑话邮件"""
        joke = self.searcher.search_jokes(1, category)[0]
        
        return {
            'subject': f"每日一笑 - {joke.get('title', '笑话')}",
            'body': self.generate_joke_text(
                count=1,
                format_type='email_format',
                category=category,
                include_metadata=True
            )
        }
    
    def get_available_formats(self) -> List[str]:
        """获取可用的文本格式"""
        return list(self.templates.keys())
    
    def get_available_categories(self) -> List[str]:
        """获取可用的笑话类别"""
        return ['any', 'programming', 'dad', 'general']
    
    def save_jokes_to_file(self, 
                          filename: str,
                          count: int = 10,
                          category: str = 'any',
                          format_type: str = 'markdown') -> str:
        """
        保存笑话到文件
        
        Args:
            filename: 文件名
            count: 笑话数量
            category: 笑话类别
            format_type: 文本格式
            
        Returns:
            保存的文件路径
        """
        jokes_text = self.generate_joke_text(count, format_type, category, True)
        
        # 添加文件头信息
        header = f"""# 笑话收集
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
类别: {category}
数量: {count}
格式: {format_type}

"""
        
        full_content = header + jokes_text
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"笑话已保存到文件: {filename}")
        return filename

def main():
    """测试函数"""
    generator = JokeGenerator()
    
    print("=== 生成单个笑话 ===")
    joke = generator.generate_joke_text(count=1, format_type='full_format')
    print(joke)
    print()
    
    print("=== 生成随机笑话 ===")
    random_joke = generator.generate_random_joke()
    print(random_joke)
    print()
    
    print("=== 生成论坛帖子 ===")
    forum_post = generator.generate_joke_for_forum('programming')
    print(forum_post)
    print()
    
    print("=== 生成社交媒体内容 ===")
    social_media = generator.generate_joke_for_social_media('dad')
    print(social_media)
    print()
    
    print("=== 生成笑话合集 ===")
    collection = generator.generate_joke_collection(['programming', 'dad'], 2)
    print(collection)
    print()
    
    print("=== 生成邮件 ===")
    email = generator.generate_joke_email('any')
    print(f"主题: {email['subject']}")
    print(f"内容: {email['body']}")

if __name__ == "__main__":
    main()
