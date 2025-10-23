# Auto Discuz - ZelosTech 论坛自动化工具

这是一个基于 Background Agents 的 Discuz 论坛自动化工具，专门为 ZelosTech 论坛 (http://bbs.zelostech.com.cn) 设计，可以自动访问论坛、回复主题、创建新主题等操作。

## 目标论坛
- **论坛地址**: http://bbs.zelostech.com.cn/forum.php?gid=1
- **账户**: yurisun
- **功能**: 自动回复、自动发帖、定时任务

## 功能特性

- 🤖 **自动回复**：自动检测新主题并进行智能回复
- 📝 **自动发帖**：定时创建新主题，保持论坛活跃度
- ⏰ **定时任务**：支持自定义时间间隔和调度
- 🔒 **安全登录**：支持用户名密码登录
- 📊 **日志记录**：详细的操作日志和错误追踪
- 🎯 **智能随机**：随机延迟和内容，避免被检测

## 技术架构

- **Selenium WebDriver**：模拟浏览器操作
- **BeautifulSoup**：HTML 解析
- **Schedule**：定时任务调度
- **Requests**：HTTP 请求处理
- **Background Agents**：后台持续运行

## 快速开始

### 1. 环境配置

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env_example.txt .env
# 编辑 .env 文件，填写您的论坛信息
```

### 2. 配置说明

项目已预配置 ZelosTech 论坛信息，无需额外配置。如需修改，可编辑 `config.py` 文件：

```python
# 论坛基本信息
FORUM_URL = 'http://bbs.zelostech.com.cn'
USERNAME = 'yurisun'
PASSWORD = 'sunyuting0'

# 自动化设置
AUTO_REPLY_ENABLED = True
AUTO_CREATE_TOPIC_ENABLED = True

# 定时任务设置
REPLY_CHECK_INTERVAL = 300  # 5分钟检查一次
TOPIC_CREATE_SCHEDULE = '09:00,15:00,21:00'  # 每天3次发帖
```

### 3. 运行方式

#### 方式一：使用 Background Agent（推荐）

1. 在 Cursor 中按 `Ctrl + '` 打开 Background Agent
2. 选择此项目，Background Agent 会自动：
   - 安装依赖
   - 启动论坛自动化服务
   - 启动定时任务调度

#### 方式二：本地运行

```bash
# 快速启动（推荐）
python start_automation.py

# 测试连接
python test_connection.py

# 运行主程序（自动回复 + 创建主题）
python main.py

# 仅自动回复
python main.py --mode reply

# 仅创建主题
python main.py --mode create

# 只执行一次
python main.py --once

# 运行定时调度器
python scheduler.py
```

## 使用 Background Agents 的优势

1. **持续运行**：无需保持本地电脑开机，Background Agent 在云端持续运行
2. **环境隔离**：不影响本地开发环境
3. **自动重启**：出现错误时自动重启服务
4. **资源管理**：自动管理依赖和运行环境
5. **监控方便**：通过 Cursor 界面实时查看运行状态

## GitHub Actions 后台运行

### 设置步骤

1. **配置Secrets**
   
   在GitHub仓库设置中添加以下Secrets：
   - `FORUM_USERNAME`: 论坛用户名
   - `FORUM_PASSWORD`: 论坛密码

2. **工作流说明**

   - **`timed-reply.yml`**: 短时间运行（1小时），适合测试
   - **`continuous-reply.yml`**: 长时间运行（6小时），适合生产环境

3. **触发方式**

   - **定时触发**: 每天上午9点自动运行
   - **手动触发**: 在GitHub Actions页面手动启动
   - **代码推送**: 修改相关文件时自动触发

4. **运行参数**

   手动触发时可以自定义：
   - 回复间隔（秒）
   - 目标帖子URL
   - 最大运行时间（小时）

### 使用方法

1. **启用工作流**
   ```bash
   # 推送代码到GitHub
   git add .
   git commit -m "Add GitHub Actions workflows"
   git push origin main
   ```

2. **手动运行**
   - 访问GitHub仓库的Actions页面
   - 选择对应的工作流
   - 点击"Run workflow"按钮
   - 设置运行参数（可选）

3. **查看日志**
   - 在Actions页面查看运行状态
   - 下载日志文件查看详细信息
   - 监控回复数量和运行时间

### 优势

- **免费使用**: GitHub Actions提供免费的计算资源
- **自动调度**: 支持cron表达式定时运行
- **环境一致**: 每次运行都在相同的环境中
- **日志记录**: 完整的运行日志和错误追踪
- **灵活配置**: 支持多种触发方式和参数配置

## 配置详解

### 回复模板

在 `config.py` 中自定义回复内容：

```python
REPLY_TEMPLATES = [
    "感谢分享，很有用的信息！",
    "学习了，谢谢楼主！",
    "这个观点很有意思，我也有类似的想法。",
    # 添加更多模板...
]
```

### 主题模板

自定义自动创建的主题：

```python
TOPIC_TEMPLATES = [
    {
        "title": "今日技术分享",
        "content": "今天想和大家分享一些技术心得...",
        "forum_id": "2"  # 技术讨论区
    },
    # 添加更多模板...
]
```

## 安全建议

1. **合理设置频率**：避免过于频繁的操作
2. **随机延迟**：程序已内置随机延迟机制
3. **内容多样化**：使用多个回复和主题模板
4. **遵守规则**：确保符合论坛使用规则

## 日志监控

程序会生成详细的日志文件：
- `forum_automation.log`：主要操作日志
- `scheduler.log`：定时任务日志

## 故障排除

1. **登录失败**：检查用户名密码和论坛URL
2. **元素找不到**：可能是论坛结构变化，需要更新选择器
3. **网络问题**：检查网络连接和代理设置

## 注意事项

- 请遵守论坛使用规则和相关法律法规
- 建议在测试环境先验证功能
- 定期检查日志，确保程序正常运行
- 根据论坛特点调整配置参数

## 技术支持

如有问题，请查看日志文件或提交 Issue。