# 多账户定时回复机器人

这是一个支持多账户、多链接的 Discuz 论坛定时回复机器人，可以同时管理多个账户对多个帖子进行定时回复。

## 功能特性

- 🚀 **多账户支持**: 同时管理多个论坛账户
- 🎯 **多链接支持**: 每个账户可以配置多个回复目标
- ⏰ **灵活定时**: 每个链接可设置不同的回复间隔
- 📝 **模板轮换**: 支持多个回复模板自动轮换
- 🔄 **并发执行**: 多账户多链接并发运行
- 📊 **实时统计**: 显示各账户回复统计信息
- 🛡️ **错误处理**: 完善的错误处理和重试机制

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置机器人
复制配置示例文件并修改：
```bash
copy config_example.json config.json
```

编辑 `config.json` 文件，配置你的账户和回复目标。

### 3. 运行机器人
```bash
# 使用批处理文件（推荐）
run_timed_reply.bat

# 或直接运行Python脚本
python timed_reply.py

# 或使用主程序
python main.py
```

## 配置文件说明

### 基本结构
```json
{
  "forum": {
    "base_url": "http://bbs.zelostech.com.cn",
    "name": "ZelosTech论坛"
  },
  "accounts": [
    {
      "id": "account_1",
      "username": "你的用户名",
      "password": "你的密码",
      "login_method": "password",
      "enabled": true,
      "reply_targets": [
        {
          "id": "target_1",
          "url": "帖子链接",
          "name": "帖子名称",
          "enabled": true,
          "interval_seconds": 3600,
          "reply_templates": [
            "我在认真的水帖, - {timestamp}",
            "感谢分享，很有用的技术信息！ - {timestamp}"
          ],
          "current_template_index": 0
        }
      ]
    }
  ]
}
```

### 配置项说明

#### 账户配置 (accounts)
- `id`: 账户唯一标识
- `username`: 论坛用户名
- `password`: 论坛密码
- `login_method`: 登录方式（目前支持 "password"）
- `enabled`: 是否启用该账户
- `reply_targets`: 该账户的回复目标列表

#### 回复目标配置 (reply_targets)
- `id`: 目标唯一标识
- `url`: 帖子完整链接
- `name`: 帖子名称（用于显示）
- `enabled`: 是否启用该目标
- `interval_seconds`: 回复间隔（秒）
- `reply_templates`: 回复模板列表
- `current_template_index`: 当前使用的模板索引

#### 回复模板
- 支持 `{timestamp}` 占位符，会自动替换为当前时间
- 模板会自动轮换使用
- 示例：`"我在认真的水帖, - {timestamp}"`

## 使用示例

### 单账户多链接
```json
{
  "accounts": [
    {
      "id": "user1",
      "username": "张三",
      "password": "password123",
      "enabled": true,
      "reply_targets": [
        {
          "id": "post1",
          "url": "http://bbs.example.com/thread-1.html",
          "interval_seconds": 3600,
          "reply_templates": ["模板1", "模板2"]
        },
        {
          "id": "post2", 
          "url": "http://bbs.example.com/thread-2.html",
          "interval_seconds": 7200,
          "reply_templates": ["模板3", "模板4"]
        }
      ]
    }
  ]
}
```

### 多账户多链接
```json
{
  "accounts": [
    {
      "id": "user1",
      "username": "张三",
      "enabled": true,
      "reply_targets": [{"url": "链接1", "interval_seconds": 3600}]
    },
    {
      "id": "user2", 
      "username": "李四",
      "enabled": true,
      "reply_targets": [{"url": "链接2", "interval_seconds": 1800}]
    }
  ]
}
```

## 运行模式

### 批处理模式（推荐）
```bash
run_timed_reply.bat
```

### Python直接运行
```bash
python timed_reply.py
```

### 主程序模式
```bash
python main.py --config config.json
```

## 监控和统计

机器人运行时会实时显示：
- 各账户登录状态
- 回复统计信息
- 最后回复时间
- 下次回复倒计时

## 注意事项

1. **账户安全**: 请妥善保管账户密码，不要将包含真实密码的配置文件提交到版本控制
2. **回复频率**: 请合理设置回复间隔，避免过于频繁的回复
3. **论坛规则**: 请遵守论坛的使用规则和条款
4. **网络稳定**: 确保网络连接稳定，避免频繁断线

## 故障排除

### 常见问题
1. **登录失败**: 检查用户名密码是否正确
2. **找不到回复框**: 检查帖子链接是否有效
3. **浏览器启动失败**: 确保已安装Chrome浏览器和ChromeDriver

### 日志文件
查看 `timed_reply.log` 文件获取详细日志信息。

## 技术支持

如有问题，请查看日志文件或联系技术支持。