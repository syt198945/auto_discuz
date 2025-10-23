
# GitHub Secrets 配置指南

## 步骤1：访问仓库设置
1. 打开您的GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Secrets and variables" -> "Actions"

## 步骤2：添加Secrets
点击 "New repository secret" 添加以下secrets：

### FORUM_USERNAME
- Name: FORUM_USERNAME
- Value: 您的论坛用户名（例如：yurisun）

### FORUM_PASSWORD  
- Name: FORUM_PASSWORD
- Value: 您的论坛密码

## 步骤3：验证配置
添加完成后，您应该看到两个secrets：
- FORUM_USERNAME
- FORUM_PASSWORD

## 注意事项
- Secrets是加密存储的，只有您和GitHub Actions可以访问
- 不要在代码中硬编码密码
- 定期更新密码以确保安全
