#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
笑话故事模块
提供笑话搜索和文本生成功能
"""

from .joke_search import JokeSearcher
from .joke_generator import JokeGenerator
from .main import JokeStoriesApp

__version__ = "1.0.0"
__author__ = "Auto Discuz"
__description__ = "笑话故事生成器"

__all__ = [
    'JokeSearcher',
    'JokeGenerator', 
    'JokeStoriesApp'
]
