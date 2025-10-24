#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笑话搜索模块
用于从网上搜索各种类型的笑话
"""

import requests
import json
import random
import time
from typing import List, Dict, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JokeSearcher:
    """笑话搜索器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 笑话API配置
        self.joke_apis = {
            'icanhazdadjoke': {
                'url': 'https://icanhazdadjoke.com/',
                'headers': {'Accept': 'application/json'},
                'parse_func': self._parse_icanhazdadjoke
            },
            'jokeapi': {
                'url': 'https://v2.jokeapi.dev/joke/Any',
                'headers': {'Accept': 'application/json'},
                'parse_func': self._parse_jokeapi
            }
        }
        
        # 本地笑话库（备用）
        self.local_jokes = [
            "为什么程序员喜欢用深色主题？因为光明属于bug。",
            "为什么程序员总是混淆圣诞节和万圣节？因为 Oct 31 == Dec 25！",
            "一个程序员走进酒吧，点了一杯酒。然后点了第二杯，第三杯... 最后他点了无穷杯。",
            "为什么程序员喜欢用Git？因为他们总是需要回滚到之前的状态。",
            "什么是程序员最喜欢的编程语言？Python，因为它没有大括号。",
            "为什么程序员总是带着伞？因为他们在等待下雨（rain）的时候，实际上是在等待异常（exception）。",
            "一个程序员对另一个程序员说：'你的代码有bug。'另一个程序员回答：'这不是bug，这是特性！'",
            "为什么程序员总是把万圣节和圣诞节搞混？因为 Oct 31 == Dec 25！",
            "什么是程序员最喜欢的饮料？Java！",
            "为什么程序员总是带着笔记本？因为他们需要记录所有的bug。"
        ]
    
    def search_jokes(self, count: int = 5, category: str = 'any') -> List[Dict]:
        """
        搜索笑话
        
        Args:
            count: 要获取的笑话数量
            category: 笑话类别 ('any', 'programming', 'general', 'dad')
            
        Returns:
            笑话列表，每个笑话包含title, content, source字段
        """
        jokes = []
        
        # 尝试从在线API获取笑话
        for api_name, api_config in self.joke_apis.items():
            try:
                api_jokes = self._fetch_from_api(api_name, api_config, count - len(jokes))
                jokes.extend(api_jokes)
                
                if len(jokes) >= count:
                    break
                    
            except Exception as e:
                logger.warning(f"从 {api_name} 获取笑话失败: {e}")
                continue
        
        # 如果在线API获取的笑话不够，从本地库补充
        if len(jokes) < count:
            local_count = count - len(jokes)
            local_jokes = self._get_local_jokes(local_count)
            jokes.extend(local_jokes)
        
        return jokes[:count]
    
    def _fetch_from_api(self, api_name: str, api_config: Dict, count: int) -> List[Dict]:
        """从指定API获取笑话"""
        jokes = []
        
        for _ in range(count):
            try:
                response = self.session.get(
                    api_config['url'], 
                    headers=api_config['headers'],
                    timeout=10
                )
                response.raise_for_status()
                
                joke_data = response.json()
                parsed_joke = api_config['parse_func'](joke_data)
                
                if parsed_joke:
                    jokes.append(parsed_joke)
                
                # 避免请求过于频繁
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"从 {api_name} 获取单个笑话失败: {e}")
                continue
        
        return jokes
    
    def _parse_icanhazdadjoke(self, data: Dict) -> Optional[Dict]:
        """解析icanhazdadjoke API响应"""
        try:
            return {
                'title': 'Dad Joke',
                'content': data.get('joke', ''),
                'source': 'icanhazdadjoke.com'
            }
        except Exception:
            return None
    
    def _parse_jokeapi(self, data: Dict) -> Optional[Dict]:
        """解析jokeapi API响应"""
        try:
            if data.get('type') == 'single':
                content = data.get('joke', '')
            elif data.get('type') == 'twopart':
                setup = data.get('setup', '')
                delivery = data.get('delivery', '')
                content = f"{setup} {delivery}"
            else:
                return None
            
            return {
                'title': f"Joke ({data.get('category', 'Unknown')})",
                'content': content,
                'source': 'jokeapi.dev'
            }
        except Exception:
            return None
    
    def _get_local_jokes(self, count: int) -> List[Dict]:
        """从本地笑话库获取笑话"""
        selected_jokes = random.sample(self.local_jokes, min(count, len(self.local_jokes)))
        
        return [
            {
                'title': '本地笑话',
                'content': joke,
                'source': 'local_database'
            }
            for joke in selected_jokes
        ]
    
    def search_programming_jokes(self, count: int = 5) -> List[Dict]:
        """专门搜索编程相关的笑话"""
        programming_jokes = [
            "为什么程序员总是带着伞？因为他们在等待下雨（rain）的时候，实际上是在等待异常（exception）。",
            "什么是程序员最喜欢的编程语言？Python，因为它没有大括号。",
            "一个程序员对另一个程序员说：'你的代码有bug。'另一个程序员回答：'这不是bug，这是特性！'",
            "为什么程序员喜欢用深色主题？因为光明属于bug。",
            "为什么程序员总是混淆圣诞节和万圣节？因为 Oct 31 == Dec 25！",
            "什么是程序员最喜欢的饮料？Java！",
            "为什么程序员总是带着笔记本？因为他们需要记录所有的bug。",
            "一个程序员走进酒吧，点了一杯酒。然后点了第二杯，第三杯... 最后他点了无穷杯。",
            "为什么程序员喜欢用Git？因为他们总是需要回滚到之前的状态。",
            "什么是程序员最害怕的事情？没有网络连接。"
        ]
        
        selected_jokes = random.sample(programming_jokes, min(count, len(programming_jokes)))
        
        return [
            {
                'title': '编程笑话',
                'content': joke,
                'source': 'programming_jokes'
            }
            for joke in selected_jokes
        ]
    
    def search_dad_jokes(self, count: int = 5) -> List[Dict]:
        """搜索爸爸笑话"""
        dad_jokes = [
            "为什么鸡要过马路？为了证明它不是胆小鬼！",
            "什么是世界上最快的动物？猎豹！不，是光速！",
            "为什么数学书总是很伤心？因为它有太多问题。",
            "什么是世界上最长的单词？微笑，因为它有两英里长！",
            "为什么鱼不能玩扑克？因为它们总是被抓住！",
            "什么是世界上最冷的动物？企鹅！",
            "为什么鸟总是很累？因为它们总是飞得很高！",
            "什么是世界上最聪明的动物？人类！不，是海豚！",
            "为什么狗总是很饿？因为它们总是摇尾巴！",
            "什么是世界上最勇敢的动物？狮子！不，是老鼠！"
        ]
        
        selected_jokes = random.sample(dad_jokes, min(count, len(dad_jokes)))
        
        return [
            {
                'title': '爸爸笑话',
                'content': joke,
                'source': 'dad_jokes'
            }
            for joke in selected_jokes
        ]

def main():
    """测试函数"""
    searcher = JokeSearcher()
    
    print("=== 搜索一般笑话 ===")
    jokes = searcher.search_jokes(count=3)
    for i, joke in enumerate(jokes, 1):
        print(f"{i}. {joke['title']}")
        print(f"   {joke['content']}")
        print(f"   来源: {joke['source']}")
        print()
    
    print("=== 搜索编程笑话 ===")
    prog_jokes = searcher.search_programming_jokes(count=2)
    for i, joke in enumerate(prog_jokes, 1):
        print(f"{i}. {joke['title']}")
        print(f"   {joke['content']}")
        print(f"   来源: {joke['source']}")
        print()
    
    print("=== 搜索爸爸笑话 ===")
    dad_jokes = searcher.search_dad_jokes(count=2)
    for i, joke in enumerate(dad_jokes, 1):
        print(f"{i}. {joke['title']}")
        print(f"   {joke['content']}")
        print(f"   来源: {joke['source']}")
        print()

if __name__ == "__main__":
    main()
