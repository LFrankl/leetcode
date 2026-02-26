# GitHub Pages 部署指南

本文档说明如何将 LeetCode 每日题目自动发布到 GitHub Pages，实现随时随地在线查看。

## 功能说明

- **固定访问链接**：`https://你的用户名.github.io/leetcode/`
- **自动更新**：每天 16:15 自动抓取题目并推送到网站
- **历史浏览**：索引页面列出所有历史题目，可随时查看
- **移动友好**：响应式设计，手机端体验良好

## 前置准备

### 1. 检查 Git 是否已安装

```bash
git --version
```

如果未安装，请先安装 Git：
- macOS: `brew install git`
- 或访问 https://git-scm.com/download/mac

### 2. 安装 Python 依赖

```bash
cd /Users/bilibili/dev/leetcodejob
pip3 install markdown2
```

`markdown2` 用于将 Markdown 转换为 HTML。

### 3. 配置 Git 用户信息（如果之前没配置过）

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

## GitHub 仓库设置

### 步骤 1: 创建 GitHub 仓库

1. 访问 GitHub: https://github.com/new
2. 仓库名称：`leetcode`（推荐，也可以自定义）
3. 设置为 **Public**（公开仓库才能使用免费的 GitHub Pages）
4. **不要**勾选 "Add a README file"
5. 点击 "Create repository"

### 步骤 2: 获取仓库信息

创建完成后，你会看到类似这样的地址：

```
https://github.com/你的用户名/leetcode.git
```

**请记下你的 GitHub 用户名，稍后需要配置到脚本中。**

### 步骤 3: 初始化本地 Git 仓库

在项目目录执行：

```bash
cd /Users/bilibili/dev/leetcodejob

# 初始化 Git 仓库（如果还没初始化）
git init

# 添加远程仓库（替换你的用户名）
git remote add origin https://github.com/你的用户名/leetcode.git

# 设置默认分支为 main
git branch -M main
```

### 步骤 4: 配置 GitHub Personal Access Token

由于 GitHub 已不支持密码认证，需要创建 Personal Access Token (PAT)。

1. 访问 GitHub Settings: https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. Note: 填写 `LeetCode Auto Push`
4. Expiration: 选择 `No expiration`（永不过期）
5. 勾选权限：
   - ✅ **repo**（完整的仓库访问权限）
6. 点击底部 "Generate token"
7. **重要：复制生成的 token（类似 `ghp_xxxxxxxxxxxx`），妥善保存，离开页面后无法再次查看**

### 步骤 5: 配置 Git 凭证

为了避免每次推送都输入密码，配置 Token 到 Git：

```bash
# 方法一：使用 Git 凭证存储（推荐）
git config --global credential.helper store

# 首次推送时会要求输入用户名和密码：
# Username: 你的 GitHub 用户名
# Password: 刚才复制的 Personal Access Token (ghp_xxxx)
```

**或者方法二：直接在 remote URL 中包含 Token**

```bash
# 移除旧的 remote
git remote remove origin

# 添加包含 Token 的 remote（替换你的用户名和 Token）
git remote add origin https://你的Token@github.com/你的用户名/leetcode.git
```

### 步骤 6: 启用 GitHub Pages

1. 进入你的仓库页面：`https://github.com/你的用户名/leetcode`
2. 点击 **Settings** 标签
3. 左侧菜单找到 **Pages**
4. 在 "Build and deployment" 部分：
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `main`
   - **Folder**: 选择 `/docs`
5. 点击 **Save**

大约 1-2 分钟后，页面顶部会显示：

```
✅ Your site is live at https://你的用户名.github.io/leetcode/
```

## 配置说明

### 编辑 config.json

在项目根目录的 `config.json` 文件中添加 GitHub 配置：

```json
{
  "questions_per_day": 3,
  "difficulties": {
    "easy": 1,
    "medium": 1,
    "hard": 1
  },
  "output_dir": "leetcode_questions",
  "history_file": "question_history.json",
  "language": "zh-CN",

  "github_pages": {
    "enabled": true,
    "username": "你的GitHub用户名",
    "repo": "leetcode",
    "site_url": "https://你的用户名.github.io/leetcode/"
  },

  "deepseek": {
    "enabled": true,
    "api_key": "sk-cde479a2412a49439ae549fc38666ce9",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "timeout": 180,
    "prompt_template": "..."
  }
}
```

**必填字段：**
- `username`: 你的 GitHub 用户名
- `repo`: 仓库名称（通常是 `leetcode`）
- `site_url`: GitHub Pages 网站地址

## 使用流程

### 首次推送

配置完成后，手动运行一次脚本：

```bash
python3 leetcode_daily.py
```

脚本会：
1. 抓取今日 3 道题目
2. 生成 Markdown 和 HTML 文件
3. 更新索引页面
4. 自动提交到 Git
5. 推送到 GitHub

首次推送可能需要输入 GitHub 用户名和 Token（如果前面没配置凭证）。

### 查看网站

大约 1-2 分钟后，访问你的 GitHub Pages 网址：

```
https://你的用户名.github.io/leetcode/
```

你会看到：
- 一个索引页，列出所有日期的题目
- 点击日期可以查看当天的 3 道题目
- 包含完整的题目描述、代码模板和 AI 解答

### 自动定时运行

定时任务（每天 16:15）会自动执行以上流程，无需手动操作。

```bash
# 查看定时任务状态
launchctl list | grep leetcode

# 手动触发一次（用于测试）
launchctl start com.leetcode.daily
```

## 文件结构

```
leetcodejob/
├── leetcode_questions/              # Markdown 源文件（保留）
│   ├── 1_简单_两数之和_20260226.md
│   └── ...
├── docs/                            # GitHub Pages 发布目录
│   ├── index.html                  # 索引页（固定入口）
│   ├── css/
│   │   └── style.css               # 样式文件
│   ├── 20260226.html               # 2026-02-26 的题目页
│   ├── 20260227.html               # 2026-02-27 的题目页
│   └── ...
├── config.json
├── leetcode_daily.py
└── GITHUB_PAGES_SETUP.md           # 本文档
```

## 常见问题

### Q: 推送失败，提示 403 Forbidden 或认证失败？

A: 检查以下几点：
1. Personal Access Token 是否正确配置
2. Token 权限是否包含 `repo`
3. 尝试重新配置凭证：
   ```bash
   git config --global --unset credential.helper
   git config --global credential.helper store
   ```

### Q: GitHub Pages 显示 404？

A: 检查以下几点：
1. 仓库是否为 Public
2. Pages 设置中 Branch 是否选择了 `main`，Folder 是否选择了 `/docs`
3. 等待 1-2 分钟，GitHub Pages 需要时间部署

### Q: 网站显示但样式错乱？

A: 检查 `docs/css/style.css` 文件是否存在，并且已提交到 Git。

### Q: 如何删除某天的题目？

A:
1. 删除对应的 `docs/YYYYMMDD.html` 文件
2. 编辑 `docs/index.html`，删除对应的日期条目
3. 提交并推送：
   ```bash
   git add docs/
   git commit -m "Remove questions for YYYYMMDD"
   git push
   ```

### Q: 想更换 GitHub Pages 域名？

A: GitHub Pages 支持自定义域名：
1. 在仓库 Settings → Pages 中添加自定义域名
2. 配置 DNS CNAME 记录指向 `你的用户名.github.io`
3. 更新 `config.json` 中的 `site_url`

### Q: 想让仓库私有怎么办？

A: 私有仓库需要 GitHub Pro 账户才能使用 GitHub Pages。免费账户只能用公开仓库。

## 安全提示

- ✅ **Personal Access Token** 不要提交到 Git 仓库
- ✅ **DeepSeek API Key** 不要提交到 Git 仓库
- ✅ 已在 `.gitignore` 中排除 `config.json`，确保敏感信息不会上传

推送到 GitHub 的文件：
- ✅ Markdown 题目文件（公开可见，无敏感信息）
- ✅ HTML 生成文件（公开可见）
- ✅ CSS 样式文件（公开可见）
- ❌ config.json（不推送，包含 API Key）
- ❌ question_history.json（不推送，本地使用）
- ❌ execution.log（不推送，本地使用）

## 下一步

配置完成后，你可以：
1. 将固定链接添加到浏览器书签
2. 分享链接给朋友一起刷题
3. 接入推送通知（Bark/Server酱等）- 见 `PUSH_NOTIFICATION_SETUP.md`（未来实现）

祝刷题愉快！
