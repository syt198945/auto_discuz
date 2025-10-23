# GitHub Actions 后台运行指南

## 概述

本指南将帮助您在GitHub后台运行`run_timed_reply.bat`脚本，实现论坛定时回复的自动化。

## 🚀 快速开始

### 1. 运行设置脚本
```bash
python setup_github_actions.py
```

### 2. 配置GitHub Secrets
按照生成的`GITHUB_SECRETS_GUIDE.md`文件配置：
- `FORUM_USERNAME`: 论坛用户名
- `FORUM_PASSWORD`: 论坛密码

### 3. 推送代码
```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin main
```

## 📁 文件说明

### 工作流文件
- **`.github/workflows/timed-reply.yml`**: 短时间运行（1小时），适合测试
- **`.github/workflows/continuous-reply.yml`**: 长时间运行（6小时），适合生产环境

### Python脚本
- **`github_runner.py`**: 专门为GitHub Actions优化的运行器
- **`timed_reply.py`**: 原始定时回复脚本（已更新支持环境变量）

### 配置工具
- **`setup_github_actions.py`**: 快速设置和检查脚本
- **`GITHUB_SECRETS_GUIDE.md`**: Secrets配置指南

## ⚙️ 工作流配置

### 触发方式

1. **定时触发**
   - `timed-reply.yml`: 每天上午9点运行
   - `continuous-reply.yml`: 每6小时运行一次

2. **手动触发**
   - 在GitHub Actions页面手动启动
   - 可自定义运行参数

3. **代码推送触发**
   - 修改相关文件时自动触发

### 运行参数

手动触发时可设置：
- **回复间隔**: 15-3600秒（默认15秒）
- **目标帖子URL**: 自定义回复的帖子
- **最大运行时间**: 1-6小时（默认1小时）

## 🔧 使用方法

### 方法1：使用GitHub Actions（推荐）

1. **启用工作流**
   - 推送代码到GitHub
   - 工作流自动激活

2. **手动运行**
   - 访问仓库的Actions页面
   - 选择对应工作流
   - 点击"Run workflow"

3. **监控状态**
   - 查看运行日志
   - 下载日志文件
   - 监控回复数量

### 方法2：本地运行

```bash
# 运行原始脚本
run_timed_reply.bat

# 运行GitHub优化版本
python github_runner.py
```

## 📊 监控和日志

### 日志文件
- `github_timed_reply.log`: GitHub Actions运行日志
- `timed_reply.log`: 原始脚本日志
- `forum_automation.log`: 论坛操作日志

### 监控指标
- 总回复数量
- 运行时间
- 平均回复间隔
- 错误次数

## 🛠️ 故障排除

### 常见问题

1. **登录失败**
   - 检查GitHub Secrets配置
   - 验证用户名密码正确性

2. **工作流失败**
   - 查看Actions页面错误信息
   - 检查Chrome和ChromeDriver版本

3. **回复失败**
   - 检查目标帖子URL
   - 验证论坛结构是否变化

### 调试方法

1. **查看日志**
   ```bash
   # 下载日志文件
   # 在Actions页面下载artifacts
   ```

2. **本地测试**
   ```bash
   # 设置环境变量
   set FORUM_USERNAME=your_username
   set FORUM_PASSWORD=your_password
   set TARGET_URL=your_target_url
   
   # 运行测试
   python github_runner.py
   ```

## 🔒 安全建议

1. **密码安全**
   - 使用GitHub Secrets存储敏感信息
   - 定期更新密码

2. **运行频率**
   - 避免过于频繁的回复
   - 设置合理的间隔时间

3. **内容合规**
   - 确保回复内容符合论坛规则
   - 避免垃圾信息

## 📈 高级配置

### 自定义工作流

1. **修改运行时间**
   ```yaml
   schedule:
     - cron: '0 */2 * * *'  # 每2小时运行
   ```

2. **添加通知**
   ```yaml
   - name: 发送通知
     uses: 8398a7/action-slack@v3
     with:
       status: ${{ job.status }}
   ```

3. **条件运行**
   ```yaml
   if: github.ref == 'refs/heads/main'
   ```

## 🎯 最佳实践

1. **测试优先**
   - 先在测试环境验证
   - 使用短时间工作流测试

2. **监控运行**
   - 定期检查运行状态
   - 及时处理错误

3. **备份配置**
   - 保存工作流配置
   - 记录重要参数

## 📞 技术支持

如遇问题，请：
1. 查看GitHub Actions运行日志
2. 检查本地测试结果
3. 参考故障排除指南
4. 提交Issue获取帮助

---

🎉 **恭喜！** 您已成功配置GitHub Actions后台运行环境！
