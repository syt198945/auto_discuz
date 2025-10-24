#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的测试脚本
"""

from joke_search import JokeSearcher
from joke_generator import JokeGenerator

def test_basic():
    """基本测试"""
    print("=== 基本测试 ===")
    
    # 创建搜索器
    searcher = JokeSearcher()
    
    # 搜索编程笑话
    print("1. 搜索编程笑话:")
    jokes = searcher.search_programming_jokes(2)
    for i, joke in enumerate(jokes, 1):
        print(f"   {i}. {joke['content']}")
    
    # 创建生成器
    generator = JokeGenerator()
    
    # 生成简单格式的笑话
    print("\n2. 生成简单格式笑话:")
    text = generator.generate_joke_text(
        count=1, 
        format_type='simple', 
        category='programming'
    )
    print(text)
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_basic()
