# LeetCode 每日题目获取脚本

自动获取 LeetCode 题目，使用 DeepSeek AI 生成详细解答，支持历史记录追踪和定时自动运行。

## 功能特性

- **智能题目选择**: 每天自动选择简单、中等、困难各一道题（可配置）
- **历史记录管理**: 自动维护已选题目列表，避免重复
- **AI 解答生成**: 集成 DeepSeek API，自动生成多种解法和复杂度分析（Go + C++ 实现）
- **执行日志记录**: 自动记录每次执行结果，方便追踪
- **系统通知**: 执行完毕后自动弹窗通知，无需额外依赖
- **完整题目信息**: 包含题目描述、代码模板、提示和测试用例
- **定时自动运行**: 支持 macOS launchd 定时任务（默认每天下午 16:15）
- **GitHub Pages 发布**: 自动生成 HTML 并发布到 GitHub Pages，随时随地在线查看 ⭐️ **新功能**
- **灵活配置**: 通过配置文件自定义所有参数

## 快速开始（5分钟）

### 1. 安装依赖

```bash
cd /Users/bilibili/dev/leetcodejob
pip3 install requests markdown2
```

`markdown2` 用于生成 GitHub Pages HTML 页面（可选）。

### 2. 配置 API Key

编辑 `config.json` 文件，替换你的 DeepSeek API Key：

```json
{
  "deepseek": {
    "api_key": "sk-xxxxxxxxxxxxx"  // 替换这里
  }
}
```

**获取 API Key**: 访问 [DeepSeek 平台](https://platform.deepseek.com/) 注册并获取。

**不使用 AI 解答**: 如果只想获取题目，设置 `"enabled": false` 即可。

### 3. 运行脚本

```bash
python3 leetcode_daily.py
```

### 4. 查看结果

```bash
ls leetcode_questions/
```

生成的文件格式：`题号_难度_中文题目名_日期.md`

示例：
- `1_简单_两数之和_20260226.md`
- `124_困难_二叉树中的最大路径和_20260226.md`

### 5. 设置定时任务（可选）

每天自动运行：

```bash
./install.sh
```

### 6. 启用 GitHub Pages（可选）⭐️

发布到网站，随时随地在线查看题目：

```bash
# 运行配置脚本
./setup_github.sh
```

**详细步骤**: 查看 [QUICKSTART_GITHUB.md](QUICKSTART_GITHUB.md)

**你的网站地址**: https://LFrankl.github.io/leetcode/

配置完成后，每天题目会自动推送到网站，访问固定链接即可查看最新内容。

## 目录结构

```
leetcodejob/
├── leetcode_daily.py           # 主脚本
├── config.json                 # 配置文件
├── config.example.json         # 配置文件示例
├── question_history.json       # 历史记录（自动生成）
├── execution.log               # 执行日志（自动生成）
├── com.leetcode.daily.plist    # macOS 定时任务配置
├── install.sh                  # 一键安装定时任务
├── reload.sh                   # 重新加载定时任务
├── uninstall.sh                # 一键卸载定时任务
├── setup_github.sh             # GitHub Pages 配置脚本 ⭐️
├── .gitignore                  # Git 忽略文件
├── logs/                       # launchd 日志目录
├── leetcode_questions/         # 题目 Markdown 保存目录
├── docs/                       # GitHub Pages 发布目录 ⭐️
│   ├── index.html              # 索引页（固定入口）
│   ├── css/style.css           # 样式文件
│   └── YYYYMMDD.html           # 每日题目 HTML 页面
├── README.md                   # 本文档
├── CHANGELOG.md                # 更新日志
├── QUICKSTART_GITHUB.md        # GitHub Pages 快速开始 ⭐️
└── GITHUB_PAGES_SETUP.md       # GitHub Pages 详细配置 ⭐️
```

## 配置说明

编辑 `config.json` 文件自定义配置：

```json
{
  "questions_per_day": 3,           // 每天获取题目总数
  "difficulties": {
    "easy": 1,                       // 简单题数量
    "medium": 1,                     // 中等题数量
    "hard": 1                        // 困难题数量
  },
  "output_dir": "leetcode_questions",  // 保存目录
  "history_file": "question_history.json",  // 历史记录文件
  "language": "zh-CN",                 // 语言
  "deepseek": {
    "enabled": true,                   // 是否启用 DeepSeek
    "api_key": "YOUR_API_KEY",         // API Key
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",          // 使用的模型
    "timeout": 180,                    // API 超时时间（秒），默认 180 秒
    "prompt_template": "..."           // 提示词模板
  }
}
```

### 自定义难度分布

只要简单和中等题：
```json
{
  "difficulties": {
    "easy": 1,
    "medium": 1,
    "hard": 0
  }
}
```

每天获取 5 道题：
```json
{
  "difficulties": {
    "easy": 2,
    "medium": 2,
    "hard": 1
  }
}
```

### DeepSeek 提示词模板

默认提示词会要求 AI 提供：
1. 题目分析和解题思路
2. 至少 2-3 种不同的解法
3. 每种解法的 Go 和 C++ 详细代码实现
4. 时间复杂度和空间复杂度分析
5. 不同解法之间的对比和优缺点

支持的占位符：
- `{title}`: 题目标题
- `{difficulty}`: 题目难度
- `{content}`: 题目描述

## 生成文件格式

### 文件命名

**格式**: `题号_难度_中文题目名_日期.md`

**示例**:
- `1_简单_两数之和_20260226.md`
- `124_困难_二叉树中的最大路径和_20260226.md`
- `15_中等_三数之和_20260226.md`

**优势**:
- 题号在前方便排序
- 一眼看出难度
- 中文标题直观易懂

### 文件内容结构

1. **题目信息**
   - 标题和编号
   - 难度和标签
   - LeetCode 链接

2. **题目描述**
   - 完整的中文题目描述

3. **代码模板**
   - Python3, Java, C++, JavaScript, Go 等多种语言

4. **提示和测试用例**
   - 官方提示
   - 示例测试用例

5. **AI 解答 (DeepSeek)**
   - 多种解法（2-3 种）
   - Go 和 C++ 双语言实现
   - 时间/空间复杂度分析
   - 解法对比表格

## 执行日志

脚本会自动记录每次执行结果到 `execution.log` 文件。

### 日志格式

```
20260226 全部成功
20260227 第2题失败
20260228 第1题, 第3题失败
```

### 查看日志

```bash
cat execution.log
```

或查看最近 10 条：

```bash
tail -10 execution.log
```

## 使用说明

### 手动运行

```bash
python3 leetcode_daily.py
```

输出示例：
```
============================================================
LeetCode 每日题目获取脚本 (DeepSeek AI 增强版)
============================================================

历史记录: 已选择 0 道题目
DeepSeek API: 已启用 (模型: deepseek-chat)

正在获取题目列表...
✓ 共获取 4239 道题目
✓ 随机选择 3 道题目

[1/3] Easy - 1. Two Sum
  正在生成 AI 解答...
  ✓ AI 解答已生成
  ✓ 已保存: 1_简单_两数之和_20260226.md

[2/3] Medium - 2. Add Two Numbers
  正在生成 AI 解答...
  ✓ AI 解答已生成
  ✓ 已保存: 2_中等_两数相加_20260226.md

[3/3] Hard - 4. Median of Two Sorted Arrays
  正在生成 AI 解答...
  ✓ AI 解答已生成
  ✓ 已保存: 4_困难_寻找两个正序数组的中位数_20260226.md

============================================================
完成! 成功保存 3 道题目
保存位置: /Users/bilibili/dev/leetcodejob/leetcode_questions
历史记录: 累计已选择 3 道题目
============================================================
```

### 查看历史记录

历史记录保存在 `question_history.json`：

```json
{
  "selected_questions": ["1", "2", "4"],
  "last_updated": "2026-02-26 15:30:00"
}
```

### 重置历史记录

想重新开始：

```bash
rm question_history.json
```

### 定时任务管理

```bash
# 安装定时任务（每天下午 16:15 自动运行）
./install.sh

# 立即测试运行
launchctl start com.leetcode.daily

# 查看任务状态
launchctl list | grep leetcode

# 查看 launchd 日志
tail -f logs/output.log
tail -f logs/error.log

# 卸载任务
./uninstall.sh
```

**执行完毕通知**：脚本运行完成后会自动弹出系统通知："job 执行完毕"

**修改运行时间**：编辑 `com.leetcode.daily.plist` 文件中的 `Hour` 和 `Minute` 值，然后重新加载：
```bash
launchctl unload ~/Library/LaunchAgents/com.leetcode.daily.plist
launchctl load ~/Library/LaunchAgents/com.leetcode.daily.plist
```

## 常见问题

### Q: 如何获取 DeepSeek API Key？

A: 访问 [https://platform.deepseek.com/](https://platform.deepseek.com/)，注册账号后在 API Keys 页面创建。

### Q: 不使用 DeepSeek 可以吗？

A: 可以。在 `config.json` 中设置 `"enabled": false`，脚本会正常获取题目，但不会生成 AI 解答。

### Q: API 调用失败怎么办？

A: 检查以下几点：
1. API Key 是否正确
2. 账户余额是否充足
3. 网络连接是否正常
4. 查看 `execution.log` 了解具体错误

### Q: API 调用太慢或经常超时？

A:
- 默认超时时间为 **180 秒（3 分钟）**，对于复杂题目可能需要更长时间
- 如需调整，编辑 `config.json` 中的 `timeout` 值：
  ```json
  {
    "deepseek": {
      "timeout": 300  // 改为 5 分钟
    }
  }
  ```
- 如果仍然超时，脚本会自动跳过该题并保存不含 AI 解答的版本

### Q: 如何修改每天获取的题目数量和难度？

A: 编辑 `config.json` 中的 `difficulties` 配置：
```json
{
  "difficulties": {
    "easy": 2,      // 每天 2 道简单题
    "medium": 1,    // 每天 1 道中等题
    "hard": 0       // 不获取困难题
  }
}
```

### Q: 历史记录会占用很多空间吗？

A: 不会。历史记录只保存题目 ID，即使选择了 1000 道题，文件大小也只有几 KB。

### Q: 可以手动添加题目到历史记录吗？

A: 可以。直接编辑 `question_history.json` 文件，在 `selected_questions` 数组中添加题目 ID。

### Q: DeepSeek API 收费吗？

A: DeepSeek 提供免费额度，超出后按使用量收费。具体价格请查看官网。

### Q: 如何自定义 AI 解答的风格？

A: 修改 `config.json` 中的 `prompt_template`，调整提示词内容和要求。

### Q: 执行日志在哪里？

A:
- 脚本执行结果：`execution.log`
- launchd 输出日志：`logs/output.log`
- launchd 错误日志：`logs/error.log`

## 成本估算

使用 DeepSeek API 的大致成本（仅供参考）：

- 每道题目 AI 解答消耗约 3000-5000 tokens
- DeepSeek 价格：约 ¥0.001/1K tokens（输入）+ ¥0.002/1K tokens（输出）
- 每天 3 道题，月成本约 ¥1-3 元

## 技术栈

- Python 3.7+
- Requests 库
- LeetCode API
- DeepSeek API
- macOS launchd (定时任务)

## 许可

本脚本仅供学习交流使用。请遵守 LeetCode 和 DeepSeek 的服务条款。

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新记录。
