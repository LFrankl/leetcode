#!/usr/bin/env python3
"""
完全重建脚本
三层结构：日期 → 执行记录 → 题目列表 → 单个题目内容
"""

import os
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import markdown2
    MARKDOWN2_AVAILABLE = True
except ImportError:
    MARKDOWN2_AVAILABLE = False
    print("❌ markdown2 未安装")
    print("请先安装: pip3 install markdown2")
    exit(1)


def clean_old_html_files(docs_dir):
    """删除所有旧的 HTML 文件（保留 index.html）"""
    print("删除旧的 HTML 文件...")

    deleted_count = 0
    for html_file in docs_dir.glob("*.html"):
        if html_file.name != "index.html":
            try:
                html_file.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"  ⚠️ 删除失败 {html_file.name}: {e}")

    print(f"✓ 已删除 {deleted_count} 个旧文件")


def parse_markdown_file(md_file_path):
    """解析单个 markdown 文件，提取题目信息"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 从文件名提取难度：题号_难度_标题_日期.md
        filename = Path(md_file_path).stem
        parts = filename.split('_')

        difficulty = "medium"  # 默认
        if len(parts) >= 4:
            difficulty_str = parts[1]  # 第二部分是难度
            if difficulty_str in ['简单', 'Easy']:
                difficulty = 'easy'
            elif difficulty_str in ['困难', 'Hard']:
                difficulty = 'hard'
            elif difficulty_str in ['中等', 'Medium']:
                difficulty = 'medium'

        # 提取题号和标题（支持 "1. 两数之和" 和 "LCR 031. LRU 缓存" 格式）
        title_match = re.search(r'^#\s+([\w\s]+)\.\s+(.+)$', content, re.MULTILINE)
        question_number = title_match.group(1).strip() if title_match else "Unknown"
        question_title = title_match.group(2).strip() if title_match else "未知题目"

        # 提取 LeetCode 链接
        leetcode_url = ""
        url_match = re.search(r'https://leetcode\.cn/problems/[^\s\)]+', content)
        if url_match:
            leetcode_url = url_match.group(0)

        return {
            'number': question_number,
            'title': question_title,
            'difficulty': difficulty,
            'content': content,
            'url': leetcode_url
        }

    except Exception as e:
        print(f"  ⚠️ 解析失败 {md_file_path}: {e}")
        return None


def generate_question_html(question_info, record_id, question_index, date_str, time_str, docs_dir):
    """生成单个题目的 HTML 文件"""

    # 转换 Markdown 为 HTML
    html_body = markdown2.markdown(
        question_info['content'],
        extras=['fenced-code-blocks', 'tables', 'header-ids']
    )

    # 格式化日期时间
    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"

    # 生成文件名
    html_filename = f"{record_id}_q{question_index}.html"
    html_file = docs_dir / html_filename

    # 难度中文映射
    difficulty_map = {
        'easy': '简单',
        'medium': '中等',
        'hard': '困难'
    }
    difficulty_cn = difficulty_map.get(question_info['difficulty'], '未知')

    # 生成完整 HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{question_info['number']}. {question_info['title']} - LeetCode</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- 顶部导航栏 -->
    <div class="top-bar">
        <button class="menu-button" onclick="history.back()" aria-label="返回">
            <div class="menu-icon">
                <span style="transform: rotate(-45deg) translateY(-2px);"></span>
                <span style="transform: rotate(45deg) translateY(2px);"></span>
            </div>
        </button>
        <div class="logo">
            <span class="logo-emoji">📚</span>
            LeetCode 每日题目
        </div>
        <div class="update-time">{formatted_date} {formatted_time}</div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content" style="margin-left: 0;">
        <div class="content-wrapper">
            <button class="back-button" onclick="history.back()">
                ← 返回题目列表
            </button>

            <div class="question-card">
                <div class="question-header">
                    <span class="question-number">{question_info['number']}. {question_info['title']}</span>
                    <span class="difficulty-badge difficulty-{question_info['difficulty']}">
                        {difficulty_cn}
                    </span>
                    {f'<a href="{question_info["url"]}" target="_blank" class="question-link">在 LeetCode 打开</a>' if question_info['url'] else ''}
                </div>
                <div class="markdown-content">
                    {html_body}
                </div>
            </div>

            <div class="footer">
                <p>由 <a href="https://github.com/LFrankl/leetcode" target="_blank">LeetCode Daily Script</a> 自动生成</p>
                <p>AI 解答由 <a href="https://www.deepseek.com/" target="_blank">DeepSeek</a> 提供</p>
            </div>
        </div>
    </div>

    <!-- 浮动返回按钮 -->
    <button class="fab-back" onclick="history.back()" aria-label="返回题目列表">
        ↑
    </button>
</body>
</html>"""

    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        return html_filename
    except Exception as e:
        print(f"  ✗ 生成 HTML 失败: {e}")
        return None


def scan_and_group_markdown_files(questions_dir):
    """扫描并按日期分组 markdown 文件"""
    files_by_date = defaultdict(list)

    md_files = sorted(Path(questions_dir).glob("*.md"))
    print(f"发现 {len(md_files)} 个 markdown 文件")

    for md_file in md_files:
        filename = md_file.stem
        parts = filename.split('_')

        if len(parts) >= 4:
            date_str = parts[-1]
            if len(date_str) == 8 and date_str.isdigit():
                files_by_date[date_str].append(str(md_file))

    return files_by_date


def rebuild_all_records(files_by_date, docs_dir):
    """重建所有记录"""
    all_records = []

    sorted_dates = sorted(files_by_date.keys())

    for date_str in sorted_dates:
        md_files = sorted(files_by_date[date_str])
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

        print(f"\n处理 {formatted_date} ({len(md_files)} 个文件)")

        # 每4个文件一组
        group_size = 4
        total_groups = (len(md_files) + group_size - 1) // group_size

        for i in range(0, len(md_files), group_size):
            group_files = md_files[i:i+group_size]
            group_num = i // group_size + 1

            # 为每组生成不同的时间戳
            hour = i // group_size
            time_str = f"{hour:02d}0000"
            record_id = f"{date_str}_{time_str}"

            formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"

            print(f"  第 {group_num}/{total_groups} 组 (记录ID: {record_id})")

            questions = []

            # 为每道题生成独立的 HTML 文件
            for q_idx, md_file in enumerate(group_files, 1):
                question_info = parse_markdown_file(md_file)

                if question_info:
                    html_filename = generate_question_html(
                        question_info,
                        record_id,
                        q_idx,
                        date_str,
                        time_str,
                        docs_dir
                    )

                    if html_filename:
                        questions.append({
                            'number': question_info['number'],
                            'title': question_info['title'],
                            'difficulty': question_info['difficulty'],
                            'file': html_filename
                        })
                        print(f"    ✓ 题目 {q_idx}: {question_info['number']}. {question_info['title']}")

            # 添加记录
            if questions:
                all_records.append({
                    'date': f"{formatted_date} {formatted_time}",
                    'record_id': record_id,
                    'count': len(questions),
                    'questions': questions
                })

    return all_records


def update_history_json(records, docs_dir):
    """更新 history.json"""
    history_file = docs_dir / "history.json"

    try:
        # 按日期时间排序（最新的在前）
        records.sort(key=lambda x: x['date'], reverse=True)

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'records': records,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)

        print(f"✓ 已更新 history.json，共 {len(records)} 条记录")
        return True

    except Exception as e:
        print(f"✗ 更新 history.json 失败: {e}")
        return False


def update_app_js(docs_dir):
    """更新 app.js 以支持三层结构"""
    app_js_file = docs_dir / "js" / "app.js"

    new_app_js = """// LeetCode 每日题目 - Google 风格应用（三层结构）

class LeetCodeApp {
    constructor() {
        this.allRecords = [];
        this.recordsByDate = {};
        this.currentDate = null;
        this.currentView = 'list'; // 'list' or 'detail'
        this.init();
    }

    async init() {
        // 绑定事件
        this.bindEvents();

        // 加载历史数据
        await this.loadHistory();

        // 显示今天的记录列表
        if (Object.keys(this.recordsByDate).length > 0) {
            const latestDate = Object.keys(this.recordsByDate)[0];
            this.showRecordList(latestDate);
        } else {
            this.showEmptyState();
        }
    }

    bindEvents() {
        // 侧边栏切换
        const menuButton = document.getElementById('menuButton');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');

        menuButton.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('visible');
        });

        overlay.addEventListener('click', () => {
            this.closeSidebar();
        });

        // 返回按钮
        document.getElementById('backButton').addEventListener('click', () => {
            this.showRecordList(this.currentDate);
        });

        // FAB 返回按钮
        document.getElementById('fabBack').addEventListener('click', () => {
            this.showRecordList(this.currentDate);
        });

        // ESC 键关闭侧边栏
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                this.closeSidebar();
            }
        });
    }

    closeSidebar() {
        document.getElementById('sidebar').classList.remove('open');
        document.getElementById('sidebarOverlay').classList.remove('visible');
    }

    async loadHistory() {
        try {
            const response = await fetch('history.json');
            if (!response.ok) {
                throw new Error('无法加载历史记录');
            }

            const data = await response.json();
            this.allRecords = data.records || [];

            // 按日期分组
            this.groupRecordsByDate();

            // 渲染侧边栏
            this.renderSidebar();

            // 更新统计
            this.updateStats();

        } catch (error) {
            console.error('加载历史记录失败:', error);
            this.allRecords = [];
        }
    }

    groupRecordsByDate() {
        this.recordsByDate = {};

        this.allRecords.forEach(record => {
            // 提取日期部分（YYYY-MM-DD）
            const dateOnly = record.date.split(' ')[0];

            if (!this.recordsByDate[dateOnly]) {
                this.recordsByDate[dateOnly] = [];
            }

            this.recordsByDate[dateOnly].push(record);
        });
    }

    renderSidebar() {
        const historyList = document.getElementById('historyList');

        if (Object.keys(this.recordsByDate).length === 0) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📝</div>
                    <div class="empty-state-text">暂无历史记录</div>
                </div>
            `;
            return;
        }

        // 按日期分组渲染
        const dates = Object.keys(this.recordsByDate).sort((a, b) => b.localeCompare(a));

        historyList.innerHTML = dates.map(date => {
            const records = this.recordsByDate[date];
            const totalCount = records.reduce((sum, r) => sum + r.count, 0);

            return `
                <div class="date-group">
                    <div class="date-group-header">${date}</div>
                    <div class="date-group-items">
                        <div class="history-item" onclick="app.selectDate('${date}')">
                            <span class="history-date">${records.length} 次执行，共 ${totalCount} 题</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    selectDate(date) {
        this.showRecordList(date);

        // 移动端自动关闭侧边栏
        if (window.innerWidth <= 768) {
            this.closeSidebar();
        }
    }

    showRecordList(date) {
        this.currentDate = date;
        this.currentView = 'list';

        const records = this.recordsByDate[date] || [];

        // 切换视图
        document.getElementById('recordListView').style.display = 'block';
        document.getElementById('questionDetailView').classList.remove('active');

        // 更新标题
        document.getElementById('contentTitle').textContent = date;
        document.getElementById('contentSubtitle').textContent =
            `共 ${records.length} 次执行`;

        // 渲染记录列表
        const recordList = document.getElementById('recordList');

        if (records.length === 0) {
            recordList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📝</div>
                    <div class="empty-state-text">该日期暂无记录</div>
                </div>
            `;
            return;
        }

        recordList.innerHTML = records.map((record, index) => {
            // 提取时间部分
            const timeOnly = record.date.split(' ')[1];

            return `
                <div class="record-card" onclick="app.viewRecord(${index}, '${date}')">
                    <div class="record-time">${timeOnly}</div>
                    <div class="record-info">共 ${record.count} 道题目</div>
                    <div class="record-arrow">→</div>
                </div>
            `;
        }).join('');
    }

    viewRecord(index, date) {
        const records = this.recordsByDate[date];
        const record = records[index];

        // 切换到详情视图（题目列表）
        this.currentView = 'detail';
        document.getElementById('recordListView').style.display = 'none';
        document.getElementById('questionDetailView').classList.add('active');

        // 更新标题
        document.getElementById('detailTitle').textContent = record.date;
        document.getElementById('detailSubtitle').textContent = `共 ${record.count} 题`;

        // 显示题目列表
        this.showQuestionList(record);

        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    showQuestionList(record) {
        const questionList = document.getElementById('questionList');

        // 难度中文映射
        const difficultyMap = {
            'easy': '简单',
            'medium': '中等',
            'hard': '困难'
        };

        // 渲染题目列表卡片
        questionList.innerHTML = record.questions.map((question, index) => {
            return `
                <div class="question-card clickable" onclick="app.viewQuestion('${question.file}')">
                    <div class="question-header">
                        <span class="question-number">${question.number}. ${question.title}</span>
                        <span class="difficulty-badge difficulty-${question.difficulty}">
                            ${difficultyMap[question.difficulty] || '未知'}
                        </span>
                        <div class="record-arrow">→</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    viewQuestion(filename) {
        // 跳转到题目详情页
        window.location.href = filename;
    }

    updateStats() {
        // 更新统计数据
        const totalQuestions = this.allRecords.reduce((sum, record) => sum + record.count, 0);
        const uniqueDates = Object.keys(this.recordsByDate).length;

        document.getElementById('totalQuestions').textContent = totalQuestions;
        document.getElementById('continuousDays').textContent = uniqueDates;

        // 更新最后更新时间
        if (this.allRecords.length > 0) {
            document.getElementById('updateTime').textContent =
                `最后更新：${this.allRecords[0].date}`;
        }
    }

    showEmptyState() {
        const recordList = document.getElementById('recordList');
        recordList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <div class="empty-state-text">暂无记录</div>
                <div class="empty-state-hint">运行脚本后，记录将自动显示在这里</div>
            </div>
        `;
    }
}

// 初始化应用
const app = new LeetCodeApp();
"""

    try:
        with open(app_js_file, 'w', encoding='utf-8') as f:
            f.write(new_app_js)
        print("✓ 已更新 app.js")
        return True
    except Exception as e:
        print(f"✗ 更新 app.js 失败: {e}")
        return False


def update_css(docs_dir):
    """更新 CSS，添加可点击题目卡片样式"""
    css_file = docs_dir / "css" / "style.css"

    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()

        # 在 .question-card 后添加 clickable 样式
        if '.question-card.clickable' not in css_content:
            additional_css = """
/* 可点击的题目卡片 */
.question-card.clickable {
    cursor: pointer;
    transition: all 0.2s;
}

.question-card.clickable:hover {
    box-shadow: var(--shadow-hover);
    border-color: var(--primary-blue);
}

.question-card.clickable .question-header {
    border-bottom: none;
    padding-bottom: 0;
    margin-bottom: 0;
}

.question-card.clickable .record-arrow {
    margin-left: auto;
    font-size: 20px;
    color: var(--text-secondary);
    transition: transform 0.2s;
}

.question-card.clickable:hover .record-arrow {
    transform: translateX(4px);
    color: var(--primary-blue);
}
"""
            css_content += additional_css

            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_content)

            print("✓ 已更新 style.css")
        else:
            print("✓ style.css 已是最新")

        return True

    except Exception as e:
        print(f"✗ 更新 CSS 失败: {e}")
        return False


def git_push(total_records=0, total_questions=0):
    """提交并推送到 GitHub"""

    # 生成详细的 commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if total_records > 0 and total_questions > 0:
        commit_message = f"🔄 重建网站 | {total_records} 条记录 · {total_questions} 道题目\n\n更新时间: {timestamp}\n架构: 三层结构 (日期 → 记录 → 题目列表 → 内容)\n\n🤖 Rebuilt by rebuild_all.py"
    else:
        commit_message = f"🔄 重建网站\n\n更新时间: {timestamp}\n\n🤖 Rebuilt by rebuild_all.py"

    commands = [
        ['git', 'add', 'docs/'],
        ['git', 'commit', '-m', commit_message],
        ['git', 'push', 'origin', 'main']
    ]

    try:
        for cmd in commands:
            print(f"  执行: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                if 'nothing to commit' in result.stdout or 'nothing to commit' in result.stderr:
                    print(f"  ℹ️  没有需要提交的变更")
                    continue
                else:
                    print(f"  ✗ 命令失败: {result.stderr}")
                    return False

        print(f"✓ 已推送到 GitHub")
        return True

    except Exception as e:
        print(f"✗ Git 操作失败: {e}")
        return False


def main():
    print("=" * 60)
    print("LeetCode 完全重建脚本")
    print("三层结构：日期 → 执行记录 → 题目列表 → 单个题目内容")
    print("=" * 60)
    print()

    # 配置
    questions_dir = Path("leetcode_questions")
    docs_dir = Path("docs")

    if not questions_dir.exists():
        print("❌ leetcode_questions 目录不存在")
        return

    docs_dir.mkdir(parents=True, exist_ok=True)

    # 1. 清理旧文件
    print("步骤 1: 清理旧的 HTML 文件...")
    clean_old_html_files(docs_dir)
    print()

    # 2. 扫描 markdown 文件
    print("步骤 2: 扫描 markdown 文件...")
    files_by_date = scan_and_group_markdown_files(questions_dir)

    if not files_by_date:
        print("❌ 没有找到需要处理的文件")
        return

    print()

    # 3. 重建所有记录
    print("步骤 3: 重建所有记录...")
    all_records = rebuild_all_records(files_by_date, docs_dir)
    print()
    print(f"✓ 成功生成 {len(all_records)} 条记录")
    print()

    # 4. 更新 history.json
    print("步骤 4: 更新 history.json...")
    update_history_json(all_records, docs_dir)
    print()

    # 5. 更新 app.js
    print("步骤 5: 更新 app.js...")
    update_app_js(docs_dir)
    print()

    # 6. 更新 CSS
    print("步骤 6: 更新 CSS...")
    update_css(docs_dir)
    print()

    # 7. 推送到 GitHub
    print("步骤 7: 推送到 GitHub...")

    # 计算统计信息
    total_questions = sum(r['count'] for r in all_records)
    total_files = sum(len(r['questions']) for r in all_records)

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            github_enabled = config.get('github_pages', {}).get('enabled', False)
    except:
        github_enabled = False

    if github_enabled:
        git_push(len(all_records), total_questions)
    else:
        print("  ⚠️  GitHub Pages 未启用，跳过推送")

    print()
    print("=" * 60)
    print("重建完成！")
    print("=" * 60)
    print()
    print(f"生成记录: {len(all_records)} 条")
    print(f"题目总数: {total_questions} 题")
    print(f"HTML 文件: {total_files} 个")
    print()
    print("你可以访问 https://LFrankl.github.io/leetcode/ 查看效果")
    print()


if __name__ == "__main__":
    main()
