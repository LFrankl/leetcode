# 更新日志

## v2.2 (2026-02-26)

### 新增功能

#### 执行日志记录
- 新增 `execution.log` 文件，自动记录每次执行结果
- 日志格式：`yyyymmdd 全部成功` 或 `yyyymmdd 第X题失败`
- 方便追踪脚本执行历史和失败情况

#### 系统通知
- 新增 macOS 系统通知功能
- 脚本执行完毕后自动弹窗通知："job 执行完毕"
- 使用原生 AppleScript 实现，无需额外依赖

#### 定时任务优化
- 默认执行时间改为每天下午 16:00（之前为上午 9:00）
- 更符合日常使用习惯

#### API 超时时间优化
- DeepSeek API 超时时间从 60 秒增加到 **180 秒（3 分钟）**
- 支持通过配置文件自定义超时时间
- 更好地支持复杂题目的 AI 解答生成

### 优化内容

#### 项目清理
- 删除重复的 `setup.sh` 脚本（功能已整合到 `install.sh`）
- 删除 `test.sh` 脚本（功能简单，不再需要）
- 删除 `QUICKSTART.md`（内容已整合到 `README.md`）
- 清理备份文件夹

#### 文档整合
- 将快速开始指南整合到 `README.md`
- 简化文档结构，只保留 `README.md` 和 `CHANGELOG.md`
- 添加执行日志使用说明

#### 项目结构优化
最终项目结构：
```
leetcodejob/
├── leetcode_daily.py           # 主脚本
├── config.json                 # 配置文件
├── config.example.json         # 配置示例
├── question_history.json       # 历史记录
├── execution.log               # 执行日志
├── com.leetcode.daily.plist    # 定时任务配置
├── install.sh                  # 安装脚本
├── uninstall.sh                # 卸载脚本
├── .gitignore                  # Git 配置
├── logs/                       # launchd 日志
├── leetcode_questions/         # 题目目录
├── README.md                   # 使用文档
└── CHANGELOG.md                # 本文件
```

---

## v2.1 (2026-02-26)

### 优化内容

#### 1. 文件命名格式优化
- **旧格式**: `日期_题号_英文slug.md`
  - 例如：`2026-02-26_124_binary-tree-maximum-path-sum.md`

- **新格式**: `题号_难度_中文题目名_日期.md`
  - 例如：`124_困难_二叉树中的最大路径和_20260226.md`

**优势**:
- 一眼看出题目难度
- 中文标题更直观
- 题号在前方便排序和查找
- 日期格式更简洁（yyyymmdd）

#### 2. AI 解答代码语言优化
- **旧要求**: 只提供 Python 代码实现
- **新要求**: 同时提供 Go 和 C++ 两种语言的实现

**提示词模板更新**:
```
请提供：
1. 题目分析和解题思路
2. 至少 2-3 种不同的解法（如果适用）
3. 每种解法的详细代码实现（同时提供 Go 和 C++ 两种语言的实现）
4. 每种解法的时间复杂度和空间复杂度分析
5. 不同解法之间的对比和优缺点
```

**AI 解答示例结构**:
```markdown
## 解法一：xxx
### Go 实现
```go
// Go 代码
```
### C++ 实现
```cpp
// C++ 代码
```
### 复杂度分析
- 时间复杂度：O(n)
- 空间复杂度：O(1)
```

### 测试结果

测试脚本成功生成 3 道题目，包含：
- ✅ 简单题 1 道
- ✅ 中等题 1 道
- ✅ 困难题 1 道

第一道题成功生成了完整的 AI 解答，包含：
- 3 种不同的解法
- 每种解法的 Go 和 C++ 实现
- 详细的复杂度分析
- 解法对比表格

---

## v2.0 (2026-02-26)

### 新增功能
- ✅ 添加 DeepSeek AI 集成
- ✅ 添加历史记录管理，避免重复
- ✅ 改进题目选择逻辑（按难度各选一道）
- ✅ 优化错误处理和日志输出

### 配置说明

新增配置项：
```json
{
  "difficulties": {
    "easy": 1,
    "medium": 1,
    "hard": 1
  },
  "history_file": "question_history.json",
  "deepseek": {
    "enabled": true,
    "api_key": "YOUR_API_KEY",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "prompt_template": "..."
  }
}
```

---

## v1.0 (2026-02-26)

### 初始版本

#### 基础功能
- ✅ 从 LeetCode 获取题目列表
- ✅ 随机选择指定难度的题目
- ✅ 保存题目为 Markdown 格式
- ✅ 支持 macOS launchd 定时任务

#### 支持的内容
- 题目描述（中文）
- 多种语言的代码模板
- 示例测试用例
- 官方提示

#### 文件结构
- `leetcode_daily.py` - 主脚本
- `config.json` - 配置文件
- `install.sh` / `uninstall.sh` - 定时任务管理
- `README.md` - 使用文档

---

## 未来计划

### v3.0 计划
- [ ] 支持题目标签筛选
- [ ] 支持题目通过率筛选
- [ ] 添加题目收藏功能
- [ ] 支持多个 AI 模型选择
- [ ] 添加题目统计分析

### 待优化
- [ ] 优化 API 超时处理
- [ ] 添加网络重试机制
- [ ] 支持英文题目选项
- [ ] 添加题目难度统计

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

如有建议或发现 Bug，请在项目中提交 Issue。
