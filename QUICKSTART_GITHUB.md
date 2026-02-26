# GitHub Pages 快速开始（5步搞定）

你的 GitHub 用户名：**LFrankl**
你的网站地址：**https://LFrankl.github.io/leetcode/**

---

## 第一步：在 GitHub 创建仓库（2分钟）

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `leetcode`
   - **Public** ✅（必须公开才能免费使用 GitHub Pages）
   - **不要**勾选 "Add a README file"
3. 点击 "Create repository"

---

## 第二步：创建 Personal Access Token（2分钟）

1. 访问 https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写：
   - **Note**: `LeetCode Auto Push`
   - **Expiration**: `No expiration`（永不过期）
   - **勾选权限**: ✅ `repo`（完整的仓库访问权限）
4. 点击底部 **"Generate token"**
5. **重要**：复制生成的 Token（格式：`ghp_xxxxxxxxxxxxxxxxxxxx`）
   - 这个 Token 只显示一次，请妥善保存
   - 等会儿第一次推送时需要用到

---

## 第三步：配置本地 Git（1分钟）

在项目目录运行配置脚本：

```bash
cd /Users/bilibili/dev/leetcodejob
./setup_github.sh
```

脚本会自动：
- ✅ 初始化 Git 仓库
- ✅ 添加远程仓库地址
- ✅ 配置凭证存储

---

## 第四步：安装依赖并测试（3分钟）

```bash
# 安装 markdown2 库（用于生成 HTML）
pip3 install markdown2

# 测试运行脚本
python3 leetcode_daily.py
```

**首次运行会提示输入 GitHub 凭证：**

```
Username for 'https://github.com': LFrankl
Password for 'https://LFrankl@github.com': ghp_xxxxxxxxxxxxxxxxxxxx
```

- **Username**: `LFrankl`
- **Password**: 粘贴第二步复制的 Token

输入后会保存凭证，以后不再需要输入。

**预期输出：**

```
============================================================
LeetCode 每日题目获取脚本 (DeepSeek AI 增强版)
============================================================

历史记录: 已选择 X 道题目
DeepSeek API: 已启用 (模型: deepseek-chat)

正在获取题目列表...
✓ 共获取 4239 道题目
✓ 随机选择 3 道题目

[1/3] Easy - 1. Two Sum
  正在生成 AI 解答...
  ✓ AI 解答已生成
  ✓ 已保存: 1_简单_两数之和_20260226.md

...

============================================================
完成! 成功保存 3 道题目
保存位置: /Users/bilibili/dev/leetcodejob/leetcode_questions
历史记录: 累计已选择 X 道题目
============================================================

正在生成 GitHub Pages...
  ✓ 已生成 HTML: 20260226.html
  ✓ 已更新索引页面

正在推送到 GitHub...
  执行: git add docs/
  执行: git add leetcode_questions/
  执行: git commit -m Add LeetCode questions for 2026-02-26
  执行: git push origin main
  ✓ 已推送到 GitHub
  🌐 访问: https://LFrankl.github.io/leetcode/

============================================================
```

---

## 第五步：启用 GitHub Pages（1分钟）

1. 访问你的仓库设置页面：
   https://github.com/LFrankl/leetcode/settings/pages

2. 在 **"Build and deployment"** 部分：
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `main`
   - **Folder**: 选择 `/docs`

3. 点击 **"Save"**

4. 等待 1-2 分钟，页面顶部会显示：
   ```
   ✅ Your site is live at https://LFrankl.github.io/leetcode/
   ```

---

## 完成！🎉

现在你可以：

1. **访问你的网站**：https://LFrankl.github.io/leetcode/
2. **保存到书签**：这是固定链接，每天自动更新
3. **分享给朋友**：链接是公开的，任何人都可以访问

---

## 日常使用

### 自动执行（推荐）

定时任务每天 16:15 自动运行，无需任何操作：

```bash
# 查看定时任务状态
launchctl list | grep leetcode

# 手动触发一次（测试用）
launchctl start com.leetcode.daily
```

### 手动执行

```bash
cd /Users/bilibili/dev/leetcodejob
python3 leetcode_daily.py
```

执行后会：
1. 抓取 3 道新题目（简单、中等、困难各一道）
2. 生成 Markdown 和 HTML 文件
3. 自动推送到 GitHub
4. 1-2 分钟后网站自动更新

---

## 常见问题

### Q: 推送失败，提示认证错误？

**A**: Token 可能过期或输入错误，重新配置：

```bash
# 清除旧凭证
rm ~/.git-credentials

# 重新运行脚本（会提示输入新的 Token）
python3 leetcode_daily.py
```

### Q: 网站显示 404？

**A**: 检查以下几点：
1. 仓库是否为 Public
2. GitHub Pages 设置是否正确（Branch: main, Folder: /docs）
3. 等待 1-2 分钟让 GitHub Pages 部署完成

### Q: 脚本运行报错 "ModuleNotFoundError: No module named 'markdown2'"？

**A**: 安装依赖：

```bash
pip3 install markdown2
```

### Q: 如何关闭 GitHub Pages 推送？

**A**: 编辑 `config.json`，设置：

```json
{
  "github_pages": {
    "enabled": false
  }
}
```

### Q: 想要自定义域名？

**A**:
1. 在仓库 Settings → Pages 中添加自定义域名
2. 配置 DNS CNAME 记录指向 `LFrankl.github.io`
3. 更新 `config.json` 中的 `site_url`

---

## 下一步

✅ **基础功能已完成**
- 每日自动抓取题目
- AI 解答生成
- 自动发布到网站

🔔 **可选增强**（未来实现）
- 接入推送通知（Bark/Server酱/Telegram）
- 每天收到链接推送到手机
- 详见未来的 `PUSH_NOTIFICATION_SETUP.md`

---

## 需要帮助？

查看详细文档：
- `README.md` - 完整功能说明
- `GITHUB_PAGES_SETUP.md` - 详细部署指南
- `CHANGELOG.md` - 版本更新记录

祝刷题愉快！🚀
