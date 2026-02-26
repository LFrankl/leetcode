# LeetCode Daily 项目开发文档

本文档记录了 LeetCode Daily 项目从构思到完成的全部开发历程、技术决策、文件说明和经验总结。

---

## 📋 目录

1. [项目概述](#项目概述)
2. [开发历程](#开发历程)
3. [架构演进](#架构演进)
4. [文件结构说明](#文件结构说明)
5. [技术栈](#技术栈)
6. [关键技术决策](#关键技术决策)
7. [使用指南](#使用指南)
8. [问题与解决方案](#问题与解决方案)
9. [经验总结](#经验总结)
10. [未来改进方向](#未来改进方向)

---

## 项目概述

**LeetCode Daily** 是一个自动化工具，用于每天抓取 LeetCode 题目并生成 AI 解答方案。

### 核心功能

1. **自动抓取题目**：每天定时（16:15）抓取 LeetCode 3 道题目（简单、中等、困难各一道）
2. **AI 生成解答**：使用 DeepSeek API 生成详细的解题思路和代码实现
3. **多格式输出**：保存为 Markdown 文件，并转换为精美的 HTML 页面
4. **GitHub Pages 托管**：通过 GitHub Pages 展示所有题目历史记录
5. **三层导航架构**：日期 → 执行记录 → 题目列表 → 题目详情
6. **系统通知**：执行完成后发送 macOS 系统通知
7. **日志记录**：详细的执行日志，便于调试和追踪

### 项目特点

- **全自动化**：使用 macOS launchd 守护进程，无需手动干预
- **渐进式增强**：支持失败重试机制，确保数据完整性
- **美观的 UI**：Google Material Design 风格，响应式设计
- **数据持久化**：使用 JSON 文件记录所有历史数据
- **去重机制**：自动避免重复抓取相同题目

---

## 开发历程

### 第一阶段：基础功能实现（初始版本）

**目标**：创建一个能够自动抓取 LeetCode 题目并生成解答的脚本。

#### 核心功能开发

1. **题目抓取模块**
   - 使用 Selenium + Chrome 无头浏览器
   - 通过 GraphQL API 查询题目数据
   - 支持中文界面，抓取中文题目描述
   - 实现了去重逻辑，避免重复题目

2. **AI 解答生成**
   - 集成 DeepSeek API（OpenAI 兼容接口）
   - 设计了详细的 prompt，包含：
     - 题目理解
     - 解题思路（中文）
     - 多种解法对比（暴力解 vs 优化解）
     - 代码实现（Python、JavaScript、Java、C++）
     - 时间和空间复杂度分析
     - 测试用例

3. **文件保存**
   - Markdown 格式保存到 `leetcode_questions/` 目录
   - 文件命名规则：`题号_难度_标题_日期.md`

4. **定时任务**
   - 使用 macOS launchd 创建定时任务
   - 每天 16:15 自动执行
   - 配置文件：`com.leetcode.daily.plist`

5. **系统通知**
   - 使用 `osascript` 发送 macOS 通知
   - 通知内容包含执行结果和题目数量

#### 遇到的问题

**问题 1：题号提取失败**
- 现象：某些题目的题号无法正确提取（如 "LCR 031"）
- 原因：正则表达式只匹配纯数字题号
- 解决：修改正则表达式支持 "LCR XXX" 格式：`r'^([\w\s]+)\.'`

**问题 2：重复题目**
- 现象：同一个题目被多次抓取
- 原因：随机抓取算法没有排除已存在的题目
- 解决：增加 `question_history.json` 记录所有已抓取题目

**问题 3：Markdown 转 HTML 格式问题**
- 现象：代码块渲染不正确
- 原因：markdown2 库默认不启用代码高亮
- 解决：使用 `extras=['fenced-code-blocks', 'tables']` 参数

### 第二阶段：HTML 页面和 GitHub Pages 集成

**目标**：将 Markdown 文件转换为精美的 HTML 页面，并通过 GitHub Pages 发布。

#### 关键开发

1. **HTML 生成器**
   - 创建 `HTMLGenerator` 类
   - 将 Markdown 转换为 HTML
   - 添加 Google Material Design 样式
   - 实现响应式布局

2. **GitHub Pages 集成**
   - 在 `docs/` 目录生成 HTML 文件
   - 自动 git 提交和推送
   - 配置 GitHub 仓库启用 Pages（从 main 分支的 /docs 目录）

3. **历史记录页面**
   - 创建 `index.html` 主页
   - 使用 `history.json` 记录所有执行历史
   - 实现日期选择器，查看历史题目

#### 架构决策

**单文件合并架构（第一版）**
- 每次执行生成一个 HTML 文件
- 包含当天所有题目（通常 3 道）
- 文件命名：`YYYYMMDD_HHMMSS.html`
- history.json 结构：
  ```json
  {
    "date": "2026-02-26 19:55:57",
    "html_file": "20260226_195557.html",
    "count": 3
  }
  ```

**问题**：
- 用户无法直接跳转到某个具体题目
- 无法按题目难度筛选
- 不支持单独分享某道题目链接

### 第三阶段：三层架构重构

**目标**：重新设计数据结构和页面架构，实现更灵活的导航系统。

#### 架构设计

**三层导航结构**
```
第一层：日期列表（按日期分组）
  ↓
第二层：当天的执行记录（支持一天多次执行）
  ↓
第三层：题目列表（显示每道题目的预览信息）
  ↓
第四层：题目详情页（独立的 HTML 文件）
```

#### 数据结构变更

**新的 history.json 结构**
```json
{
  "records": [
    {
      "date": "2026-02-26 19:55:57",
      "record_id": "20260226_195557",
      "count": 3,
      "questions": [
        {
          "number": "2836",
          "title": "在传球游戏中最大化函数值",
          "difficulty": "hard",
          "file": "20260226_195557_q1.html"
        },
        {
          "number": "1775",
          "title": "通过最少操作次数使数组的和相等",
          "difficulty": "medium",
          "file": "20260226_195557_q2.html"
        }
      ]
    }
  ]
}
```

**关键改进**：
1. 增加 `record_id` 字段，唯一标识每次执行
2. 增加 `questions` 数组，包含每道题目的完整元数据
3. 每道题目有独立的 HTML 文件
4. 支持一天多次执行的场景

#### 文件命名规则

**题目文件**：`YYYYMMDD_HHMMSS_q{N}.html`
- `YYYYMMDD_HHMMSS`：执行的日期和时间（record_id）
- `q{N}`：题目序号（q1, q2, q3...）

**示例**：
- `20260226_195557_q1.html` - 2026年2月26日 19:55:57 执行的第1道题
- `20260226_195557_q2.html` - 同一次执行的第2道题

#### UI/UX 设计

**首页（index.html）**
- 左侧侧边栏：日期列表，显示每天的执行次数和题目总数
- 主区域：显示选中日期的所有执行记录卡片
- 每个记录卡片显示：
  - 执行时间
  - 题目数量
  - 题目预览列表（题号、标题、难度标签）

**题目详情页**
- 顶部导航栏：返回按钮、题目标题、LeetCode 链接
- 主内容区：题目描述、解题思路、代码实现
- 浮动按钮（FAB）：快速返回列表

**响应式设计**
- 移动端：侧边栏自动折叠，通过汉堡菜单打开
- 桌面端：侧边栏始终显示

#### 重构过程

**步骤 1：创建迁移脚本 `rebuild_all.py`**
- 读取所有 Markdown 文件
- 为每道题目生成独立 HTML 文件
- 重建 history.json 数据结构
- 生成新的 index.html 和 app.js

**步骤 2：更新 `leetcode_daily.py`**

完全重写了 `HTMLGenerator` 类：

1. **新增方法**：
   - `parse_markdown_file(md_file_path)` - 解析单个 Markdown 文件，提取题号、标题、难度
   - `generate_question_html(question_info, record_id, question_index, date_str, time_str)` - 生成单个题目的 HTML 文件

2. **修改方法**：
   - `convert_markdown_to_html()` - 返回 questions 列表，而不是单个文件名
   - `update_history_json()` - 使用新的数据结构

3. **移除方法**：
   - `update_index_page()` - 不再需要，由前端 JavaScript 动态渲染

**步骤 3：前端开发（app.js）**

```javascript
class LeetCodeApp {
  constructor() {
    this.allRecords = [];
    this.recordsByDate = {};
    this.currentDate = null;
    this.currentView = 'list'; // 'list' or 'detail'
  }

  // 按日期分组
  groupRecordsByDate() {
    this.allRecords.forEach(record => {
      const dateOnly = record.date.split(' ')[0];
      if (!this.recordsByDate[dateOnly]) {
        this.recordsByDate[dateOnly] = [];
      }
      this.recordsByDate[dateOnly].push(record);
    });
  }

  // 显示记录列表（第二层）
  showRecordList(date) {
    const records = this.recordsByDate[date];
    // 渲染记录卡片，每个卡片显示题目预览
  }

  // 查看记录详情（第三层：题目列表）
  viewRecord(index, date) {
    const record = records[index];
    // 渲染题目列表卡片
  }

  // 查看题目详情（跳转到独立页面）
  viewQuestion(filename) {
    window.location.href = filename;
  }
}
```

**步骤 4：数据迁移**
- 运行 `rebuild_all.py` 处理所有历史数据
- 生成 35 个题目 HTML 文件（8次执行 × 平均4道题）
- 更新 history.json 到新格式
- 验证数据完整性

**步骤 5：Git 提交**
```bash
git add docs/
git commit -m "架构重构：实现三层导航系统"
git push
```

#### 遇到的问题

**问题 1：架构不一致**
- 现象：用户本地运行 `leetcode_daily.py` 后，生成的是旧格式文件（`20260226_195557.html`）
- 原因：`leetcode_daily.py` 的 `HTMLGenerator` 类没有更新到新架构
- 解决：完全重写 `HTMLGenerator` 类，移除旧的单文件逻辑

**问题 2：重复记录**
- 现象：history.json 中出现重复的记录
- 原因：迁移脚本运行多次，每次都添加记录
- 解决：手动清理 history.json，确保唯一性

**问题 3：浏览器缓存问题**
- 现象：网页显示重复或空白卡片
- 原因：浏览器缓存了旧版本的 history.json
- 解决：在 `fetch()` 请求中添加时间戳参数防止缓存
  ```javascript
  fetch(`history.json?t=${Date.now()}`)
  ```

**问题 4：题号解析错误**
- 现象：无法正确提取 "LCR 031" 格式的题号
- 原因：正则表达式假设题号是纯数字
- 解决：修改正则表达式支持字母和数字混合
  ```python
  title_match = re.search(r'^#\s+([\w\s]+)\.\s+(.+)', content, re.MULTILINE)
  ```

### 第四阶段：项目清理和文档完善

**目标**：清理临时脚本，完善文档，确保项目的可维护性。

#### 清理工作

**删除的临时脚本**：
- `migrate_existing_files.py` - 数据迁移脚本（一次性）
- `regroup_migration.py` - 分组迁移脚本（一次性）
- `rebuild_all.py` - 重建脚本（一次性）
- `fix_today_questions.py` - 修复今日题目脚本（一次性）

**保留的核心文件**：
- `leetcode_daily.py` - 主程序
- `com.leetcode.daily.plist` - launchd 配置
- `config.json` - 配置文件（API 密钥、GitHub 凭据）
- `docs/` - GitHub Pages 目录

#### 文档创建

1. **README.md** - 项目介绍和快速开始
2. **QUICKSTART_GITHUB.md** - GitHub 仓库配置指南
3. **GITHUB_PAGES_SETUP.md** - GitHub Pages 详细配置
4. **UI_UPDATE.md** - UI 更新日志
5. **CHANGELOG.md** - 版本更新记录
6. **claude.md**（本文档） - 完整开发文档

---

## 架构演进

### 架构对比

| 特性 | 旧架构（单文件） | 新架构（三层） |
|------|-----------------|---------------|
| 文件数量 | 1个HTML/执行 | N个HTML（1个/题目） |
| 导航层级 | 2层 | 4层 |
| URL 分享 | 不支持单题分享 | 支持单题 URL |
| 数据结构 | 扁平化 | 嵌套结构 |
| 灵活性 | 低 | 高 |
| 可扩展性 | 差 | 好 |

### 架构图

```
旧架构：
Date List → HTML File (contains all questions)

新架构：
Date List → Record List → Question List → Question Detail
   ↓            ↓              ↓               ↓
侧边栏      记录卡片       题目卡片      独立HTML页面
```

---

## 文件结构说明

```
leetcodejob/
├── leetcode_daily.py              # 核心主程序
├── config.json                    # 配置文件（API密钥、Git凭据）
├── config.example.json            # 配置文件模板
├── com.leetcode.daily.plist       # macOS launchd 定时任务配置
├── question_history.json          # 已抓取题目历史（去重用）
│
├── leetcode_questions/            # Markdown 源文件目录
│   ├── 1_简单_两数之和_20260226.md
│   ├── 2836_困难_在传球游戏中最大化函数值_20260226.md
│   └── ...
│
├── docs/                          # GitHub Pages 发布目录
│   ├── index.html                 # 主页（容器）
│   ├── history.json               # 历史记录数据
│   │
│   ├── css/
│   │   └── style.css             # 全局样式（Material Design）
│   │
│   ├── js/
│   │   └── app.js                # 前端应用逻辑
│   │
│   └── 20260226_195557_q1.html   # 题目详情页
│       20260226_195557_q2.html
│       ...
│
├── README.md                      # 项目介绍
├── QUICKSTART_GITHUB.md          # GitHub 快速配置
├── GITHUB_PAGES_SETUP.md         # GitHub Pages 详细配置
├── UI_UPDATE.md                  # UI 更新日志
├── CHANGELOG.md                  # 版本更新记录
└── claude.md                     # 本文档（开发历程）
```

### 核心文件详解

#### 1. `leetcode_daily.py`

**作用**：主程序，负责题目抓取、AI 生成、HTML 转换、Git 推送

**主要类和方法**：

```python
class LeetCodeFetcher:
    """LeetCode 题目抓取器"""

    def __init__(self, config_path='config.json')
        # 初始化配置、WebDriver

    def get_random_questions(self, count=3)
        # 随机获取题目（简单、中等、困难各一道）

    def call_deepseek_api(self, question_data)
        # 调用 DeepSeek API 生成解答

    def save_markdown(self, question_data, solution, date_str)
        # 保存为 Markdown 文件

class HTMLGenerator:
    """HTML 生成器（三层架构）"""

    def parse_markdown_file(self, md_file_path)
        # 解析 Markdown 文件，提取题号、标题、难度

    def generate_question_html(self, question_info, record_id, question_index, date_str, time_str)
        # 生成单个题目的 HTML 文件

    def convert_markdown_to_html(self, md_files, date_str, time_str)
        # 转换所有 Markdown 为 HTML，返回 questions 列表

    def update_history_json(self, date_str, time_str, questions)
        # 更新 history.json（新格式）

class GitManager:
    """Git 管理器"""

    def commit_and_push(self, message)
        # 提交并推送到 GitHub
```

**执行流程**：
```python
1. 加载配置（config.json）
2. 初始化 Chrome WebDriver（无头模式）
3. 获取随机题目（3道，去重）
4. 为每道题目调用 DeepSeek API 生成解答
5. 保存为 Markdown 文件
6. 转换为 HTML 文件（每道题目一个文件）
7. 更新 history.json
8. Git 提交并推送
9. 发送系统通知
10. 清理资源（关闭浏览器）
```

#### 2. `docs/js/app.js`

**作用**：前端应用逻辑，实现三层导航

**核心类**：

```javascript
class LeetCodeApp {
    constructor() {
        this.allRecords = [];         // 所有记录
        this.recordsByDate = {};      // 按日期分组的记录
        this.currentDate = null;      // 当前选中的日期
        this.currentView = 'list';    // 当前视图：'list' 或 'detail'
    }

    async loadHistory() {
        // 加载 history.json（带缓存破坏）
        fetch(`history.json?t=${Date.now()}`)
    }

    groupRecordsByDate() {
        // 按日期分组记录
    }

    renderSidebar() {
        // 渲染左侧边栏（日期列表）
    }

    showRecordList(date) {
        // 显示某个日期的所有执行记录（第二层）
    }

    viewRecord(index, date) {
        // 查看某次执行的题目列表（第三层）
    }

    viewQuestion(filename) {
        // 跳转到题目详情页（第四层）
        window.location.href = filename;
    }
}
```

**关键实现**：

1. **缓存破坏**：
   ```javascript
   fetch(`history.json?t=${Date.now()}`)
   ```
   防止浏览器缓存旧数据

2. **按日期分组**：
   ```javascript
   const dateOnly = record.date.split(' ')[0]; // "2026-02-26 19:55:57" -> "2026-02-26"
   if (!this.recordsByDate[dateOnly]) {
       this.recordsByDate[dateOnly] = [];
   }
   this.recordsByDate[dateOnly].push(record);
   ```

3. **动态渲染记录卡片**：
   ```javascript
   recordList.innerHTML = records.map((record, index) => {
       const questionsHTML = record.questions.map(q => `
           <div class="record-question-item">
               <span class="record-question-number">${q.number}.</span>
               <span class="record-question-title">${q.title}</span>
               <span class="record-question-difficulty ${q.difficulty}">
                   ${difficultyMap[q.difficulty]}
               </span>
           </div>
       `).join('');

       return `
           <div class="record-card" onclick="app.viewRecord(${index}, '${date}')">
               <div class="record-header">
                   <div class="record-time">${timeOnly}</div>
                   <div class="record-info">共 ${record.count} 道题目</div>
               </div>
               <div class="record-questions">${questionsHTML}</div>
           </div>
       `;
   }).join('');
   ```

#### 3. `docs/css/style.css`

**作用**：全局样式，Material Design 风格

**设计系统**：

```css
/* Google Material Design 颜色 */
--primary-color: #1976d2;        /* 主色（蓝色）*/
--primary-dark: #1565c0;         /* 深蓝色 */
--accent-color: #ff4081;         /* 强调色（粉色）*/
--text-primary: #212121;         /* 主要文本 */
--text-secondary: #757575;       /* 次要文本 */
--divider: #e0e0e0;              /* 分割线 */
--background: #fafafa;           /* 背景色 */
--surface: #ffffff;              /* 表面色（卡片） */

/* Material Design 阴影 */
--shadow-1: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
--shadow-2: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
--shadow-3: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
```

**组件样式**：

1. **卡片（Card）**：
   - 白色背景
   - 圆角 8px
   - 阴影 shadow-1
   - hover 时提升阴影（shadow-2）

2. **难度徽章（Difficulty Badge）**：
   - 简单：绿色背景
   - 中等：橙色背景
   - 困难：红色背景
   - 圆角胶囊形状

3. **浮动按钮（FAB）**：
   - 固定在右下角
   - 圆形，56px × 56px
   - 强调色背景
   - 阴影 shadow-3

4. **响应式布局**：
   ```css
   @media (max-width: 768px) {
       .sidebar {
           transform: translateX(-100%);  /* 隐藏侧边栏 */
       }
       .sidebar.open {
           transform: translateX(0);       /* 显示侧边栏 */
       }
   }
   ```

#### 4. `docs/history.json`

**作用**：记录所有执行历史和题目元数据

**数据结构**：

```json
{
  "records": [
    {
      "date": "2026-02-26 19:55:57",          // 执行时间
      "record_id": "20260226_195557",         // 唯一标识符
      "count": 3,                              // 题目数量
      "questions": [                           // 题目列表
        {
          "number": "2836",                    // 题号
          "title": "在传球游戏中最大化函数值",  // 标题
          "difficulty": "hard",                // 难度
          "file": "20260226_195557_q1.html"   // HTML 文件名
        }
      ]
    }
  ],
  "last_updated": "2026-02-26 20:06:36"      // 最后更新时间
}
```

**字段说明**：
- `date`：执行的完整时间（YYYY-MM-DD HH:MM:SS）
- `record_id`：唯一标识符（YYYYMMDD_HHMMSS），用于文件命名
- `count`：本次执行的题目数量
- `questions`：题目数组，包含每道题目的完整元数据
  - `number`：题号（支持 "1", "2836", "LCR 031" 等格式）
  - `title`：题目标题（中文）
  - `difficulty`：难度（easy/medium/hard）
  - `file`：对应的 HTML 文件名
- `last_updated`：history.json 的最后更新时间

#### 5. `config.json`

**作用**：存储敏感配置信息

**结构**：

```json
{
  "deepseek_api_key": "sk-xxxxxxxxxxxxx",
  "github": {
    "username": "your-username",
    "token": "ghp_xxxxxxxxxxxxx",
    "repo_url": "https://github.com/username/leetcode.git"
  }
}
```

**注意事项**：
- 此文件包含敏感信息，已加入 `.gitignore`
- 使用 `config.example.json` 作为模板
- GitHub Token 需要 `repo` 权限

#### 6. `com.leetcode.daily.plist`

**作用**：macOS launchd 定时任务配置

**配置内容**：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.leetcode.daily</string>

    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/path/to/leetcode_daily.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>16</integer>
        <key>Minute</key>
        <integer>15</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/path/to/leetcode_daily.log</string>

    <key>StandardErrorPath</key>
    <string>/path/to/leetcode_daily_error.log</string>
</dict>
</plist>
```

**关键配置**：
- `Label`：任务唯一标识符
- `ProgramArguments`：执行的命令（Python 解释器路径 + 脚本路径）
- `StartCalendarInterval`：定时规则（每天 16:15）
- `StandardOutPath`：标准输出日志路径
- `StandardErrorPath`：错误日志路径

**安装方法**：
```bash
# 复制到 LaunchAgents 目录
cp com.leetcode.daily.plist ~/Library/LaunchAgents/

# 加载任务
launchctl load ~/Library/LaunchAgents/com.leetcode.daily.plist

# 查看任务状态
launchctl list | grep leetcode
```

#### 7. `question_history.json`

**作用**：记录所有已抓取过的题目（去重用）

**数据结构**：

```json
{
  "2836": {
    "title": "在传球游戏中最大化函数值",
    "difficulty": "hard",
    "fetched_dates": ["2026-02-26"]
  },
  "1": {
    "title": "两数之和",
    "difficulty": "easy",
    "fetched_dates": ["2026-02-26"]
  }
}
```

**用途**：
- 在随机选择题目时，排除已抓取的题目
- 记录每道题目的抓取历史
- 支持按难度过滤

#### 8. Markdown 文件（`leetcode_questions/`）

**作用**：源数据，保存题目描述和 AI 生成的解答

**文件命名**：`题号_难度_标题_日期.md`

**示例**：`2836_困难_在传球游戏中最大化函数值_20260226.md`

**内容结构**：

```markdown
# 2836. 在传球游戏中最大化函数值

## 题目描述

[题目的完整描述...]

## 解题思路

### 理解题意
...

### 解法分析

#### 方法一：暴力解法
...

#### 方法二：优化解法（推荐）
...

## 代码实现

### Python
\`\`\`python
def solution():
    ...
\`\`\`

### JavaScript
\`\`\`javascript
function solution() {
    ...
}
\`\`\`

### Java
\`\`\`java
class Solution {
    ...
}
\`\`\`

### C++
\`\`\`cpp
class Solution {
public:
    ...
};
\`\`\`

## 复杂度分析

- 时间复杂度：O(n)
- 空间复杂度：O(1)

## 测试用例

\`\`\`
输入：[1,2,3]
输出：6
解释：...
\`\`\`
```

#### 9. HTML 题目详情页（`docs/YYYYMMDD_HHMMSS_qN.html`）

**作用**：展示单个题目的完整内容

**文件结构**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>2836. 在传球游戏中最大化函数值</title>
    <!-- Material Design 样式 -->
    <style>...</style>
</head>
<body>
    <!-- 顶部导航栏 -->
    <div class="navbar">
        <button class="back-button" onclick="history.back()">
            <span class="back-arrow">←</span> 返回
        </button>
        <h1>2836. 在传球游戏中最大化函数值</h1>
        <a href="https://leetcode.cn/problems/..." target="_blank">
            在 LeetCode 上查看
        </a>
    </div>

    <!-- 主内容 -->
    <div class="container">
        <div class="content">
            <!-- Markdown 转换的 HTML 内容 -->
            ...
        </div>
    </div>

    <!-- 浮动返回按钮 -->
    <button class="fab" onclick="history.back()">
        <span class="fab-icon">←</span>
    </button>
</body>
</html>
```

**特点**：
- 完全独立的 HTML 文件，可以直接分享链接
- 包含返回按钮（浏览器 history.back()）
- 响应式设计，移动端友好
- 代码高亮显示

---

## 技术栈

### 后端（Python）

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 主编程语言 |
| Selenium | 4.x | Web 自动化（抓取题目） |
| ChromeDriver | - | Chrome 无头浏览器驱动 |
| requests | 2.x | HTTP 请求（DeepSeek API） |
| markdown2 | 2.x | Markdown → HTML 转换 |
| pathlib | - | 路径操作 |
| json | - | 数据序列化 |
| datetime | - | 时间处理 |
| subprocess | - | 执行系统命令（Git、通知） |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| HTML5 | - | 页面结构 |
| CSS3 | - | 样式（Material Design） |
| JavaScript ES6 | - | 前端逻辑 |
| Fetch API | - | 异步加载数据 |
| LocalStorage | - | （未来）缓存数据 |

### 基础设施

| 技术 | 用途 |
|------|------|
| Git | 版本控制 |
| GitHub | 代码托管 |
| GitHub Pages | 静态网站托管 |
| macOS launchd | 定时任务调度 |
| osascript | macOS 系统通知 |

### API 服务

| 服务 | 用途 |
|------|------|
| DeepSeek API | AI 生成解题方案 |
| LeetCode GraphQL API | 查询题目数据 |

---

## 关键技术决策

### 1. 为什么选择 Selenium 而不是纯 API？

**原因**：
- LeetCode 的 GraphQL API 需要登录认证
- 使用 Selenium 可以模拟真实用户行为，避免反爬虫
- 可以直接获取页面上的所有数据（题目描述、示例等）

**权衡**：
- 优点：稳定性高，不易被封禁
- 缺点：速度较慢，依赖浏览器

### 2. 为什么选择 DeepSeek 而不是 GPT-4？

**原因**：
- DeepSeek API 兼容 OpenAI 接口，易于集成
- 成本更低（相比 GPT-4）
- 代码生成能力强
- 支持中文，更适合 LeetCode 中文站

### 3. 为什么使用 launchd 而不是 cron？

**原因**：
- launchd 是 macOS 的原生任务调度器
- 比 cron 更可靠（在系统唤醒后会补执行错过的任务）
- 更好的日志管理
- 支持更复杂的调度规则

**权衡**：
- 优点：与 macOS 深度集成
- 缺点：只能在 macOS 上使用（Linux 需要改用 systemd）

### 4. 为什么使用 GitHub Pages 而不是独立服务器？

**原因**：
- 免费托管
- 自动 HTTPS
- 与 Git 工作流无缝集成
- 高可用性（GitHub 的 CDN）
- 无需维护服务器

**权衡**：
- 优点：零成本，高可靠性
- 缺点：仅支持静态网站，无法运行后端代码

### 5. 为什么采用三层架构而不是单页应用（SPA）？

**原因**：
- 更好的 SEO（每个题目有独立 URL）
- 支持直接分享单个题目链接
- 降低首页加载时间（不需要加载所有题目内容）
- 更符合传统网页浏览习惯

**权衡**：
- 优点：灵活性高，可扩展性强
- 缺点：文件数量多（每道题目一个 HTML）

### 6. 为什么使用 JSON 而不是数据库？

**原因**：
- 数据量小（每天几道题，一年也就上千条记录）
- GitHub Pages 不支持数据库
- JSON 文件可以直接托管在 GitHub
- 便于版本控制和备份

**权衡**：
- 优点：简单、轻量、易于维护
- 缺点：查询效率低（数据量大时）

---

## 使用指南

### 首次安装

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/leetcodejob.git
cd leetcodejob
```

#### 2. 安装依赖

```bash
pip3 install selenium requests markdown2
```

#### 3. 安装 ChromeDriver

```bash
# macOS (Homebrew)
brew install chromedriver

# 验证安装
chromedriver --version
```

#### 4. 配置 API 和 GitHub

复制配置模板：
```bash
cp config.example.json config.json
```

编辑 `config.json`：
```json
{
  "deepseek_api_key": "sk-your-api-key",
  "github": {
    "username": "your-github-username",
    "token": "ghp_your-personal-access-token",
    "repo_url": "https://github.com/your-username/leetcode.git"
  }
}
```

**获取 DeepSeek API Key**：
1. 访问 https://platform.deepseek.com/
2. 注册账号
3. 在控制台创建 API Key

**获取 GitHub Personal Access Token**：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 Token

#### 5. 初始化 Git 仓库

```bash
cd /path/to/leetcodejob
git init
git remote add origin https://github.com/your-username/leetcode.git
```

#### 6. 配置 GitHub Pages

1. 在 GitHub 上创建仓库 `leetcode`
2. 进入仓库设置：Settings → Pages
3. 选择 Source：`main` 分支，`/docs` 目录
4. 点击 Save

#### 7. 测试运行

```bash
python3 leetcode_daily.py
```

检查：
- `leetcode_questions/` 目录是否生成了 Markdown 文件
- `docs/` 目录是否生成了 HTML 文件
- `docs/history.json` 是否更新
- GitHub 仓库是否有新提交

#### 8. 配置定时任务

编辑 `com.leetcode.daily.plist`，替换路径：
```xml
<string>/opt/homebrew/bin/python3</string>
<string>/Users/yourusername/leetcodejob/leetcode_daily.py</string>
<string>/Users/yourusername/leetcodejob/leetcode_daily.log</string>
<string>/Users/yourusername/leetcodejob/leetcode_daily_error.log</string>
```

加载任务：
```bash
cp com.leetcode.daily.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.leetcode.daily.plist
```

验证：
```bash
launchctl list | grep leetcode
```

### 日常使用

#### 查看日志

```bash
tail -f leetcode_daily.log
```

#### 手动运行

```bash
python3 leetcode_daily.py
```

#### 查看定时任务状态

```bash
launchctl list | grep leetcode
```

#### 停止定时任务

```bash
launchctl unload ~/Library/LaunchAgents/com.leetcode.daily.plist
```

#### 访问网站

等待 1-2 分钟后，访问：
```
https://your-username.github.io/leetcode/
```

### 故障排查

#### 问题 1：ChromeDriver 版本不匹配

**错误信息**：
```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX
```

**解决方案**：
```bash
# 更新 Chrome 浏览器
# 更新 ChromeDriver
brew upgrade chromedriver

# 或手动下载对应版本
# https://chromedriver.chromium.org/downloads
```

#### 问题 2：GitHub 推送失败

**错误信息**：
```
remote: Permission to user/repo.git denied
```

**解决方案**：
1. 检查 `config.json` 中的 GitHub Token 是否正确
2. 确认 Token 有 `repo` 权限
3. 尝试手动推送测试：
   ```bash
   git push https://username:token@github.com/username/repo.git
   ```

#### 问题 3：DeepSeek API 调用失败

**错误信息**：
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
```

**解决方案**：
1. 检查 API Key 是否正确
2. 确认账户余额充足
3. 测试 API Key：
   ```bash
   curl https://api.deepseek.com/v1/chat/completions \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}'
   ```

#### 问题 4：网页显示空白

**可能原因**：
- 浏览器缓存
- history.json 格式错误
- JavaScript 加载失败

**解决方案**：
1. 硬刷新：`Cmd + Shift + R` (macOS) 或 `Ctrl + Shift + R` (Windows)
2. 检查 `history.json` 格式：
   ```bash
   cat docs/history.json | python3 -m json.tool
   ```
3. 检查浏览器控制台错误信息（F12）

#### 问题 5：题目重复

**现象**：同一道题目被抓取多次

**解决方案**：
1. 检查 `question_history.json` 是否正确记录
2. 手动清理重复题目：
   ```bash
   # 编辑 question_history.json，移除重复题目
   # 删除重复的 Markdown 和 HTML 文件
   ```

---

## 问题与解决方案

### 开发过程中的主要问题

#### 问题 1：题号格式不统一

**现象**：
- 普通题目：`1`, `2836` 等纯数字
- LCR 系列：`LCR 031`, `LCR 112` 等（字母 + 空格 + 数字）

**影响**：
- 正则表达式无法正确匹配
- 文件名生成错误
- history.json 数据不一致

**解决方案**：
```python
# 修改前：只匹配数字
question_number = re.search(r'^#\s+(\d+)\.\s+(.+)', content, re.MULTILINE)

# 修改后：支持字母、空格、数字
question_number = re.search(r'^#\s+([\w\s]+)\.\s+(.+)', content, re.MULTILINE)
```

**经验总结**：
- 在处理用户输入或外部数据时，要考虑各种边界情况
- 使用更宽松的正则表达式，然后进行验证
- 编写测试用例覆盖所有已知格式

#### 问题 2：浏览器缓存导致数据不更新

**现象**：
- 网页显示旧数据
- 新增的题目不显示
- 删除的记录仍然存在

**原因**：
- 浏览器缓存了 `history.json`
- 没有 Cache-Control 头
- 静态文件的默认缓存策略

**解决方案**：
```javascript
// 在 fetch 请求中添加时间戳
fetch(`history.json?t=${Date.now()}`)
```

**经验总结**：
- 静态网站的缓存问题很常见
- 使用时间戳或版本号破坏缓存
- 或者在服务器端设置 Cache-Control 头（GitHub Pages 不支持）

#### 问题 3：架构不一致导致的 Bug

**现象**：
- 本地运行生成旧格式文件
- 网页无法正确显示
- history.json 格式混乱

**原因**：
- 重构了前端架构和数据结构
- 但忘记更新主程序 `leetcode_daily.py`
- 导致新旧代码不兼容

**解决方案**：
1. 完全重写 `HTMLGenerator` 类
2. 统一数据结构（record_id + questions 数组）
3. 删除所有旧代码和临时脚本
4. 彻底测试新架构

**经验总结**：
- 重构时要确保所有相关代码同步更新
- 列出所有受影响的文件和模块
- 使用版本控制，方便回滚
- 编写测试确保新旧架构兼容（或完全切换）

#### 问题 4：Git 推送失败（认证问题）

**现象**：
```
remote: Permission denied (publickey)
fatal: Could not read from remote repository
```

**原因**：
- 使用 SSH URL 但没有配置 SSH 密钥
- GitHub 密码认证已废弃
- Personal Access Token 配置错误

**解决方案**：
```python
# 在 Git 命令中直接使用 Token
repo_url_with_auth = repo_url.replace(
    'https://',
    f'https://{username}:{token}@'
)
subprocess.run(['git', 'push', repo_url_with_auth, 'main'])
```

**经验总结**：
- GitHub 已废弃密码认证，必须使用 Token 或 SSH
- Token 需要 `repo` 权限
- 在自动化脚本中，HTTPS + Token 比 SSH 更简单
- 敏感信息（Token）不要硬编码，使用配置文件

#### 问题 5：Markdown 转 HTML 代码高亮问题

**现象**：
- 代码块没有语法高亮
- 代码格式错乱
- 表格渲染失败

**原因**：
- markdown2 默认不启用扩展功能
- 需要手动指定 extras

**解决方案**：
```python
import markdown2

html_content = markdown2.markdown(
    markdown_content,
    extras=['fenced-code-blocks', 'tables', 'code-friendly']
)
```

**经验总结**：
- 不同的 Markdown 库有不同的默认行为
- 查看文档了解可用的扩展功能
- 对于技术博客，代码高亮是必需功能

#### 问题 6：定时任务不执行

**现象**：
- launchd 任务加载成功
- 但到了设定时间不执行
- 日志文件为空

**可能原因**：
1. Python 解释器路径错误
2. 脚本路径错误
3. 没有执行权限
4. 环境变量问题

**排查步骤**：
```bash
# 1. 检查任务状态
launchctl list | grep leetcode

# 2. 手动触发任务（测试）
launchctl start com.leetcode.daily

# 3. 查看系统日志
log show --predicate 'subsystem == "com.apple.launchd"' --last 1h

# 4. 验证 Python 路径
which python3

# 5. 测试脚本执行
python3 /path/to/leetcode_daily.py
```

**解决方案**：
```xml
<!-- 使用绝对路径 -->
<key>ProgramArguments</key>
<array>
    <string>/opt/homebrew/bin/python3</string>
    <string>/Users/username/leetcodejob/leetcode_daily.py</string>
</array>

<!-- 设置工作目录 -->
<key>WorkingDirectory</key>
<string>/Users/username/leetcodejob</string>

<!-- 设置环境变量 -->
<key>EnvironmentVariables</key>
<dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
</dict>
```

**经验总结**：
- launchd 任务的环境与终端不同
- 始终使用绝对路径
- 设置正确的工作目录
- 包含必要的环境变量
- 日志输出非常重要

---

## 经验总结

### 架构设计经验

#### 1. 数据结构设计

**经验**：数据结构要为未来扩展留有余地

**示例**：从扁平结构到嵌套结构的演进

```json
// 旧结构：扁平化，扩展性差
{
  "date": "2026-02-26 19:55:57",
  "html_file": "20260226_195557.html",
  "count": 3
}

// 新结构：嵌套化，扩展性强
{
  "date": "2026-02-26 19:55:57",
  "record_id": "20260226_195557",
  "count": 3,
  "questions": [...]  // 可以添加任意元数据
}
```

**好处**：
- 支持一天多次执行
- 每道题目可以有独立的元数据
- 便于实现搜索、筛选、统计功能

#### 2. 文件命名规范

**经验**：文件名要包含足够的上下文信息

**不好的命名**：
```
q1.html
q2.html
q3.html
```

**好的命名**：
```
20260226_195557_q1.html  // 日期 + 时间 + 序号
```

**原因**：
- 避免文件名冲突
- 便于按时间排序
- 方便调试（一眼看出是哪次执行的）

#### 3. 前后端分离

**经验**：即使是静态网站，也要分离数据和展示

**实现**：
- 数据层：`history.json`（纯数据）
- 展示层：`app.js`（动态渲染）
- 样式层：`style.css`（独立样式）

**好处**：
- 数据格式变更不影响UI
- UI调整不需要重新生成数据
- 便于多端适配（Web、移动端）

#### 4. 渐进式增强

**经验**：先实现核心功能，再逐步优化

**演进路径**：
1. 第一版：单文件，功能完整
2. 第二版：多文件，导航优化
3. 第三版：三层架构，体验提升
4. 未来：搜索、筛选、统计...

**原则**：
- 每个版本都能独立工作
- 不要一次性设计过度
- 根据实际使用反馈迭代

### 代码质量经验

#### 1. 错误处理

**经验**：永远不要假设外部数据是正确的

**示例**：
```python
# 不好的做法：直接访问
question_number = match.group(1)  # 如果 match 是 None，会报错

# 好的做法：先检查
if match:
    question_number = match.group(1)
else:
    print(f"无法解析题号：{content[:100]}")
    return None
```

**要点**：
- 检查 API 返回值
- 验证文件是否存在
- 处理网络异常
- 提供有意义的错误信息

#### 2. 日志记录

**经验**：日志是调试的最好工具

**实现**：
```python
print(f"[{datetime.now()}] 开始抓取题目...")
print(f"[{datetime.now()}] 成功抓取题目 {question_number}: {title}")
print(f"[{datetime.now()}] 调用 DeepSeek API...")
print(f"[{datetime.now()}] 生成 HTML 文件: {html_file}")
```

**要点**：
- 记录关键步骤
- 包含时间戳
- 区分信息级别（INFO/WARNING/ERROR）
- 重定向到文件（launchd 日志）

#### 3. 配置管理

**经验**：敏感信息和配置分离

**实现**：
```python
# 使用配置文件
with open('config.json') as f:
    config = json.load(f)

api_key = config['deepseek_api_key']
github_token = config['github']['token']
```

**要点**：
- 敏感信息不提交到 Git
- 提供配置模板（`config.example.json`）
- 在 README 中说明配置方法
- 验证配置完整性

#### 4. 代码复用

**经验**：相似的逻辑要提取成函数

**示例**：
```python
# 不好的做法：重复代码
html1 = self.generate_html(question1, "20260226_195557", 1, "20260226", "195557")
html2 = self.generate_html(question2, "20260226_195557", 2, "20260226", "195557")
html3 = self.generate_html(question3, "20260226_195557", 3, "20260226", "195557")

# 好的做法：循环 + 函数
questions = []
for idx, md_file in enumerate(md_files, 1):
    html_file = self.generate_question_html(
        question_info, record_id, idx, date_str, time_str
    )
    questions.append(...)
```

### 工具使用经验

#### 1. Selenium

**经验**：
- 使用无头模式（headless）提高效率
- 显式等待（WebDriverWait）比隐式等待更可靠
- 及时关闭浏览器，避免资源泄漏

```python
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
try:
    # 操作...
finally:
    driver.quit()  # 确保关闭
```

#### 2. Git 自动化

**经验**：
- 每次执行后自动提交
- 提交信息要有意义
- 处理推送失败（重试机制）

```python
def commit_and_push(self, message):
    try:
        subprocess.run(['git', 'add', 'docs/'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push', repo_url_with_auth], check=True)
        print("推送成功")
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失败: {e}")
        # 可以添加重试逻辑
```

#### 3. API 调用

**经验**：
- 设置超时时间
- 实现重试机制
- 记录 API 使用量（成本控制）

```python
def call_api_with_retry(self, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60  # 60秒超时
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"API 调用失败，重试 {attempt + 1}/{max_retries}")
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise
```

### 前端开发经验

#### 1. Material Design

**经验**：使用成熟的设计系统，而不是自己发明

**资源**：
- 颜色：https://material.io/design/color/
- 阴影：https://material.io/design/environment/elevation.html
- 组件：https://material.io/components

**实现**：
```css
/* 使用 Material Design 的标准值 */
--shadow-1: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
--primary-color: #1976d2;
--accent-color: #ff4081;
```

#### 2. 响应式设计

**经验**：移动优先，然后适配桌面

**实现**：
```css
/* 默认：移动端样式 */
.sidebar {
    width: 100%;
    position: fixed;
    transform: translateX(-100%);
}

/* 桌面端：覆盖样式 */
@media (min-width: 769px) {
    .sidebar {
        width: 280px;
        position: relative;
        transform: translateX(0);
    }
}
```

#### 3. 性能优化

**经验**：
- 缓存破坏（Cache Busting）
- 按需加载（Lazy Loading）
- 减少 DOM 操作

```javascript
// 缓存破坏
fetch(`history.json?t=${Date.now()}`)

// 一次性渲染，避免多次 DOM 操作
const html = items.map(item => `...`).join('');
container.innerHTML = html;
```

---

## 未来改进方向

### 功能增强

#### 1. 搜索功能
- 按题号搜索
- 按标题搜索
- 按难度筛选
- 按日期范围筛选

**实现思路**：
```javascript
class LeetCodeApp {
    searchQuestions(keyword) {
        const results = [];
        this.allRecords.forEach(record => {
            record.questions.forEach(q => {
                if (q.number.includes(keyword) ||
                    q.title.includes(keyword)) {
                    results.push(q);
                }
            });
        });
        return results;
    }
}
```

#### 2. 统计功能
- 总题目数
- 按难度统计
- 连续天数
- 完成度趋势图

**实现思路**：
```javascript
class LeetCodeApp {
    getStatistics() {
        const stats = {
            total: 0,
            easy: 0,
            medium: 0,
            hard: 0,
            dates: Object.keys(this.recordsByDate).length
        };

        this.allRecords.forEach(record => {
            record.questions.forEach(q => {
                stats.total++;
                stats[q.difficulty]++;
            });
        });

        return stats;
    }
}
```

#### 3. 标签系统
- 为每道题目添加标签（数组、字符串、动态规划等）
- 按标签浏览
- 标签云

**数据结构**：
```json
{
  "questions": [
    {
      "number": "1",
      "title": "两数之和",
      "difficulty": "easy",
      "tags": ["数组", "哈希表"],
      "file": "..."
    }
  ]
}
```

#### 4. 收藏功能
- 标记喜欢的题目
- 创建自定义题集
- 导出题集

**实现思路**：
- 使用 LocalStorage 存储收藏状态
- 或使用 URL 参数分享题集

#### 5. 评论系统
- 集成 Giscus（GitHub Discussions）
- 在每道题目下方添加评论区
- 讨论解题思路

#### 6. 多语言支持
- 界面国际化（中文/英文）
- 切换 LeetCode 国际站/中国站
- 代码示例多语言

### 架构优化

#### 1. 使用前端框架
- 当前：Vanilla JavaScript
- 未来：Vue.js 或 React
- 好处：状态管理更清晰，组件化开发

#### 2. 构建工具
- 当前：无构建步骤
- 未来：Webpack/Vite
- 好处：模块化、压缩、Tree Shaking

#### 3. 静态站点生成器
- 当前：手动生成 HTML
- 未来：使用 VitePress/Astro
- 好处：更好的 SEO、更快的加载速度

#### 4. 数据库支持
- 当前：JSON 文件
- 未来：SQLite（如果迁移到服务器）
- 好处：更高效的查询、支持复杂的筛选

### 用户体验

#### 1. 加载动画
- 骨架屏（Skeleton）
- 进度条
- Loading 状态

#### 2. 错误提示
- 友好的错误页面
- 网络断开提示
- 重试按钮

#### 3. 键盘快捷键
- `Esc` 关闭侧边栏（已实现）
- `←/→` 上一题/下一题
- `/` 聚焦搜索框

#### 4. 暗黑模式
- 检测系统主题
- 手动切换
- 保存用户偏好

**实现思路**：
```css
@media (prefers-color-scheme: dark) {
    :root {
        --background: #121212;
        --surface: #1e1e1e;
        --text-primary: #ffffff;
    }
}
```

### 技术迁移

#### 1. 跨平台支持
- 当前：仅 macOS（launchd）
- 未来：支持 Linux（systemd）、Windows（Task Scheduler）

#### 2. Docker 化
- 创建 Dockerfile
- 一键部署
- 跨平台兼容

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "leetcode_daily.py"]
```

#### 3. GitHub Actions
- 当前：本地定时任务
- 未来：GitHub Actions 定时触发
- 好处：无需本地运行、云端自动化

```yaml
name: Daily LeetCode
on:
  schedule:
    - cron: '15 8 * * *'  # UTC 8:15 = 中国 16:15
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run script
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: python3 leetcode_daily.py
      - name: Commit and push
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add .
          git commit -m "Daily update"
          git push
```

---

## 附录

### A. 常用命令

```bash
# Python 环境
python3 --version
pip3 list
pip3 install -r requirements.txt

# Git 操作
git status
git add .
git commit -m "message"
git push

# launchd 任务
launchctl load ~/Library/LaunchAgents/com.leetcode.daily.plist
launchctl unload ~/Library/LaunchAgents/com.leetcode.daily.plist
launchctl list | grep leetcode
launchctl start com.leetcode.daily

# 日志查看
tail -f leetcode_daily.log
tail -f leetcode_daily_error.log
log show --predicate 'subsystem == "com.apple.launchd"' --last 1h

# ChromeDriver
chromedriver --version
which chromedriver
brew upgrade chromedriver

# 项目清理
rm -rf __pycache__
rm -f *.pyc
rm -f leetcode_daily.log
```

### B. 相关资源

#### API 文档
- DeepSeek API: https://platform.deepseek.com/docs
- LeetCode GraphQL: https://leetcode.cn/graphql
- GitHub API: https://docs.github.com/en/rest

#### 设计资源
- Material Design: https://material.io/design
- Google Fonts: https://fonts.google.com/
- Material Icons: https://fonts.google.com/icons

#### 技术文档
- Selenium: https://selenium-python.readthedocs.io/
- markdown2: https://github.com/trentm/python-markdown2
- launchd: https://www.launchd.info/

#### 社区
- LeetCode 中国: https://leetcode.cn/
- GitHub: https://github.com/

### C. 配置文件模板

#### config.example.json
```json
{
  "deepseek_api_key": "sk-your-api-key-here",
  "github": {
    "username": "your-github-username",
    "token": "ghp_your-personal-access-token",
    "repo_url": "https://github.com/your-username/leetcode.git"
  }
}
```

#### .gitignore
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# 配置文件
config.json

# 日志
*.log

# 系统文件
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# ChromeDriver
chromedriver
```

### D. 项目里程碑

- **2026-02-26**: 项目启动，完成基础功能
- **2026-02-26**: GitHub Pages 集成
- **2026-02-26**: 三层架构重构
- **2026-02-26**: 项目清理和文档完善

---

## 结语

这个项目从一个简单的想法（自动化 LeetCode 刷题）发展成为一个完整的系统，涵盖了：

- **后端自动化**：题目抓取、AI 生成、文件处理
- **前端展示**：Material Design、响应式设计、多层导航
- **基础设施**：Git 自动化、定时任务、GitHub Pages 托管

在开发过程中，我们：
- 从单文件架构演进到三层架构
- 从扁平数据结构升级到嵌套结构
- 解决了各种技术难题（认证、缓存、格式兼容）
- 建立了完整的文档体系

这个项目证明了：
1. **迭代优于一次性完美**：每个版本都可以工作，根据需求逐步演进
2. **架构设计的重要性**：良好的数据结构为未来扩展奠定基础
3. **工具选择的权衡**：根据实际需求选择合适的技术栈
4. **文档的价值**：详细的文档让项目可维护、可传承

希望这份文档能帮助你理解整个项目的来龙去脉，也为未来的开发提供参考。

**Happy Coding!** 🚀

---

*最后更新：2026-02-26*
*作者：Claude (Anthropic)*
*项目地址：https://github.com/your-username/leetcode*
