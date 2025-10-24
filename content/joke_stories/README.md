# 笑话故事模块 (Joke Stories)

一个用于搜索和生成各种类型笑话的Python模块。

## 功能特性

- 🔍 **多源笑话搜索**: 支持从多个在线API和本地数据库搜索笑话
- 📝 **多种文本格式**: 支持多种文本格式输出（简单、完整、论坛、社交媒体等）
- 🎭 **多种笑话类型**: 支持编程笑话、爸爸笑话、综合笑话等
- 💾 **文件保存**: 支持将笑话保存为各种格式的文件
- 🎯 **API接口**: 提供完整的API接口供其他程序调用
- 📱 **社交媒体支持**: 专门为论坛和社交媒体优化的格式

## 安装依赖

```bash
pip install requests urllib3
```

## 快速开始

### 基本使用

```python
from joke_search import JokeSearcher
from joke_generator import JokeGenerator

# 创建搜索器和生成器
searcher = JokeSearcher()
generator = JokeGenerator()

# 搜索笑话
jokes = searcher.search_jokes(count=5, category='programming')

# 生成格式化文本
text = generator.generate_joke_text(
    count=3, 
    format_type='full_format', 
    category='programming'
)
print(text)
```

### 命令行使用

```bash
# 搜索编程笑话
python main.py search --count 5 --category programming

# 生成随机笑话
python main.py random --format story_format

# 生成论坛帖子
python main.py forum --category dad

# 生成社交媒体内容
python main.py social --category programming

# 生成邮件
python main.py email --category any

# 生成笑话合集
python main.py collection --categories programming,dad --per-category 2

# 保存笑话到文件
python main.py save --filename jokes.md --count 10 --category any
```

## API参考

### JokeSearcher 类

#### 方法

- `search_jokes(count=5, category='any')`: 搜索笑话
- `search_programming_jokes(count=5)`: 搜索编程笑话
- `search_dad_jokes(count=5)`: 搜索爸爸笑话

### JokeGenerator 类

#### 方法

- `generate_joke_text(count=1, format_type='simple', category='any', include_metadata=False)`: 生成笑话文本
- `generate_joke_collection(categories=None, jokes_per_category=2, format_type='full_format')`: 生成笑话合集
- `generate_random_joke(format_type='story_format')`: 生成随机笑话
- `generate_joke_for_forum(category='any')`: 生成论坛帖子
- `generate_joke_for_social_media(category='any')`: 生成社交媒体内容
- `generate_joke_email(category='any')`: 生成邮件
- `save_jokes_to_file(filename, count=10, category='any', format_type='markdown')`: 保存笑话到文件

#### 可用格式

- `simple`: 简单格式
- `with_title`: 带标题格式
- `with_source`: 带来源格式
- `full_format`: 完整格式
- `story_format`: 故事格式
- `forum_post`: 论坛帖子格式
- `social_media`: 社交媒体格式
- `email_format`: 邮件格式
- `markdown`: Markdown格式

#### 可用类别

- `any`: 综合笑话
- `programming`: 编程笑话
- `dad`: 爸爸笑话
- `general`: 一般笑话

## 使用示例

### 示例1: 生成编程笑话

```python
from joke_generator import JokeGenerator

generator = JokeGenerator()

# 生成编程笑话
jokes = generator.generate_joke_text(
    count=3,
    format_type='full_format',
    category='programming'
)
print(jokes)
```

### 示例2: 生成论坛帖子

```python
# 生成适合论坛的笑话帖子
forum_post = generator.generate_joke_for_forum('programming')
print(forum_post)
```

### 示例3: 保存笑话到文件

```python
# 保存笑话到Markdown文件
filename = generator.save_jokes_to_file(
    filename='my_jokes.md',
    count=10,
    category='programming',
    format_type='markdown'
)
print(f"笑话已保存到: {filename}")
```

### 示例4: 生成笑话合集

```python
# 生成包含多种类型笑话的合集
collection = generator.generate_joke_collection(
    categories=['programming', 'dad'],
    jokes_per_category=3,
    format_type='markdown'
)
print(collection)
```

## 文件结构

```
content/joke_stories/
├── __init__.py          # 包初始化文件
├── joke_search.py       # 笑话搜索模块
├── joke_generator.py    # 笑话生成模块
├── main.py             # 主程序文件
├── example.py          # 使用示例
└── README.md           # 说明文档
```

## 注意事项

1. 在线API可能有时不可用，程序会自动回退到本地笑话库
2. 请合理使用API，避免过于频繁的请求
3. 本地笑话库包含中英文笑话，可以根据需要扩展
4. 所有文本输出都使用UTF-8编码

## 扩展开发

### 添加新的笑话源

在 `joke_search.py` 中的 `joke_apis` 字典中添加新的API配置：

```python
self.joke_apis['new_api'] = {
    'url': 'https://api.example.com/jokes',
    'headers': {'Accept': 'application/json'},
    'parse_func': self._parse_new_api
}
```

### 添加新的文本格式

在 `joke_generator.py` 中的 `templates` 字典中添加新格式：

```python
self.templates['new_format'] = "新格式模板: {content}"
```

## 许可证

本项目采用MIT许可证。
