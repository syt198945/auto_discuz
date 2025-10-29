# GitHub Actions 定时回复机器人使用说明

## 功能说明
这个 GitHub Actions 工作流会在每个工作日的 8:00-23:00（北京时间）持续运行 `timed_reply.py` 脚本。

## 工作时间分段
由于 GitHub Actions 有最长 6 小时的运行时间限制，我们采用了分段运行的策略：
- **第一段**：8:00-14:00（6小时）
- **第二段**：14:00-20:00（6小时）
- **第三段**：20:00-23:00（3小时）

## 配置步骤

### 1. 创建配置文件
确保你的仓库中有 `config.json` 文件（可以参考 `config_example.json`）

### 2. 配置文件设置
在 `config.json` 中添加工作时间配置：
```json
"work_hours": {
  "start_hour": 8,
  "end_hour": 23,
  "weekdays_only": true
}
```

### 3. 配置 GitHub Secrets（重要）
在 GitHub 仓库设置中添加以下 Secrets：
1. 进入仓库 Settings → Secrets and variables → Actions
2. 添加以下 Secrets：
   - `ACCOUNT_USERNAME`: 账户用户名
   - `ACCOUNT_PASSWORD`: 账户密码

### 4. 提交并推送代码
将配置文件和工作流文件提交到仓库：
```bash
git add .github/workflows/timed_reply.yml
git add config.json
git commit -m "添加 GitHub Actions 定时回复工作流"
git push
```

### 5. 启用 Actions
1. 进入仓库的 Actions 页面
2. 在左侧选择 "定时回复机器人" 工作流
3. 点击 "Run workflow" 可以手动触发测试

## 日志查看
- 每个工作流运行结束后，会自动上传日志文件
- 可以在 Actions 页面的 Artifacts 中下载日志
- 日志文件保留 7 天

## 注意事项
1. **免费账户限制**：GitHub Actions 免费账户每月有 2000 分钟运行时间限制
2. **配置文件安全**：不要在配置文件中明文存储敏感信息，使用 GitHub Secrets
3. **网络访问**：确保目标论坛可以从 GitHub Actions 访问
4. **ChromeDriver 兼容性**：工作流会自动匹配 Chrome 和 ChromeDriver 的版本

## 手动触发
你可以随时在 Actions 页面手动触发工作流进行测试。

## 停止运行
如果需要停止定时运行，可以：
1. 在配置文件 `config.json` 中将账户的 `enabled` 设置为 `false`
2. 或者禁用工作流（在 Actions 页面设置）

## 故障排查
如果工作流运行失败：
1. 检查日志文件了解错误原因
2. 确认配置文件格式正确
3. 确认 GitHub Secrets 已正确配置
4. 确认目标网站可访问

