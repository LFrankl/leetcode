#!/usr/bin/env python3
"""
LeetCode 每日题目获取脚本
每天随机获取指定难度的题目并保存为 Markdown 文件
支持 DeepSeek AI 解答生成
"""

import requests
import json
import os
import random
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import markdown2
    MARKDOWN2_AVAILABLE = True
except ImportError:
    MARKDOWN2_AVAILABLE = False
    print("警告: markdown2 未安装，HTML 生成功能将被禁用")
    print("安装命令: pip3 install markdown2")

def load_config():
    """加载配置文件"""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载配置文件失败: {e}")
        return None

def send_notification(title: str, message: str):
    """发送 macOS 系统通知"""
    try:
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        subprocess.run(['osascript', '-e', script], check=True)
    except Exception as e:
        print(f"警告: 发送通知失败: {e}")

class ExecutionLogger:
    """执行日志记录"""
    def __init__(self, log_file: str = "execution.log"):
        self.log_file = log_file
        self.date_str = datetime.now().strftime("%Y%m%d")
        self.results = []

    def add_result(self, index: int, success: bool, question_title: str = ""):
        """记录单个题目的结果"""
        self.results.append({
            'index': index,
            'success': success,
            'title': question_title
        })

    def save(self):
        """保存日志到文件"""
        if not self.results:
            return

        # 生成日志信息
        failed_items = [f"第{r['index']}题" for r in self.results if not r['success']]

        if failed_items:
            log_msg = f"{self.date_str} {', '.join(failed_items)}失败\n"
        else:
            log_msg = f"{self.date_str} 全部成功\n"

        # 追加到日志文件
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg)
        except Exception as e:
            print(f"警告: 保存执行日志失败: {e}")

class QuestionHistory:
    """题目历史记录管理"""
    def __init__(self, history_file: str):
        self.history_file = history_file
        self.history = self.load()

    def load(self) -> List[str]:
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('selected_questions', [])
            except Exception as e:
                print(f"警告: 加载历史记录失败: {e}")
        return []

    def save(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'selected_questions': self.history,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告: 保存历史记录失败: {e}")

    def add(self, question_id: str):
        """添加题目到历史记录"""
        if question_id not in self.history:
            self.history.append(question_id)
            self.save()

    def contains(self, question_id: str) -> bool:
        """检查题目是否已存在"""
        return question_id in self.history

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_selected': len(self.history)
        }

class DeepSeekAPI:
    """DeepSeek API 调用"""
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', False)
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', 'https://api.deepseek.com/v1')
        self.model = config.get('model', 'deepseek-chat')
        self.prompt_template = config.get('prompt_template', '')
        self.timeout = config.get('timeout', 180)  # 默认 180 秒（3 分钟）

    def is_available(self) -> bool:
        """检查 API 是否可用"""
        if not self.enabled:
            return False
        if not self.api_key or self.api_key == 'YOUR_DEEPSEEK_API_KEY_HERE':
            return False
        return True

    def generate_solution(self, question: Dict) -> Optional[str]:
        """生成题目解答"""
        if not self.is_available():
            return None

        # 清理 HTML 标签
        content = re.sub(r'<[^>]+>', '', question.get('content', ''))
        content = re.sub(r'\s+', ' ', content).strip()

        # 填充提示词
        prompt = self.prompt_template.format(
            title=question.get('title', ''),
            difficulty=question.get('difficulty', ''),
            content=content[:2000]  # 限制长度
        )

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 4000
        }

        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
            print(f"  ⚠ DeepSeek API 超时（超过 {self.timeout} 秒）")
            return None
        except Exception as e:
            print(f"  ⚠ DeepSeek API 调用失败: {e}")
            return None

class LeetCodeFetcher:
    """LeetCode 题目获取"""
    def __init__(self):
        self.base_url = "https://leetcode.cn/graphql"
        self.api_url = "https://leetcode.cn/api/problems/all/"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": "https://leetcode.cn/problemset/all/"
        }

    def get_all_questions(self) -> List[Dict]:
        """获取所有题目列表"""
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            questions = []
            for q in data.get('stat_status_pairs', []):
                stat = q.get('stat', {})
                difficulty_map = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
                questions.append({
                    'questionId': str(stat.get('question_id', '')),
                    'questionFrontendId': str(stat.get('frontend_question_id', '')),
                    'title': stat.get('question__title_slug', '').replace('-', ' ').title(),
                    'titleSlug': stat.get('question__title_slug', ''),
                    'difficulty': difficulty_map.get(q.get('difficulty', {}).get('level', 1), 'Easy'),
                    'topicTags': []
                })

            return questions
        except Exception as e:
            print(f"获取题目列表失败: {e}")
            return []

    def get_question_detail(self, title_slug: str) -> Optional[Dict]:
        """获取题目详情"""
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                translatedTitle
                translatedContent
                difficulty
                topicTags {
                    name
                    translatedName
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                sampleTestCase
                hints
            }
        }
        """

        variables = {"titleSlug": title_slug}

        try:
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            if 'errors' in data:
                return None

            question = data.get("data", {}).get("question")
            if not question:
                return None

            if question.get('translatedTitle'):
                question['title'] = question['translatedTitle']
            if question.get('translatedContent'):
                question['content'] = question['translatedContent']

            for tag in question.get('topicTags', []):
                if tag.get('translatedName'):
                    tag['name'] = tag['translatedName']

            return question
        except Exception as e:
            print(f"  获取详情失败: {e}")
            return None

def filter_by_difficulty(questions: List[Dict], difficulty: str) -> List[Dict]:
    """按难度筛选题目"""
    return [q for q in questions if q['difficulty'] == difficulty]

def select_questions_by_difficulty(
    all_questions: List[Dict],
    difficulty_config: Dict,
    history: QuestionHistory
) -> List[Dict]:
    """按难度选择题目，避免重复"""
    selected = []

    for difficulty, count in difficulty_config.items():
        difficulty_key = difficulty.capitalize()
        available = filter_by_difficulty(all_questions, difficulty_key)

        # 排除历史记录中的题目
        available = [q for q in available if not history.contains(q['questionId'])]

        if len(available) < count:
            print(f"  ⚠ {difficulty_key} 难度可用题目不足 ({len(available)}/{count})")
            count = len(available)

        if count > 0:
            selected.extend(random.sample(available, count))

    return selected

def save_as_markdown(
    question: Dict,
    ai_solution: Optional[str],
    output_dir: str
) -> bool:
    """保存题目和解答为 Markdown 文件"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 生成文件名：题目号_难度_中文题目名_日期.md
    date_str = datetime.now().strftime("%Y%m%d")

    # 清理中文标题，移除特殊字符
    chinese_title = question['title']
    # 移除不适合文件名的字符
    chinese_title = re.sub(r'[<>:"/\\|?*]', '', chinese_title)
    chinese_title = chinese_title.strip()

    # 难度映射
    difficulty_map = {'Easy': '简单', 'Medium': '中等', 'Hard': '困难'}
    difficulty_cn = difficulty_map.get(question['difficulty'], question['difficulty'])

    filename = f"{question['questionFrontendId']}_{difficulty_cn}_{chinese_title}_{date_str}.md"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"  题目已存在，跳过: {filename}")
        return False

    content = f"""# {question['questionFrontendId']}. {question['title']}

**难度**: {question['difficulty']}

**标签**: {', '.join([tag['name'] for tag in question.get('topicTags', [])])}

**链接**: https://leetcode.cn/problems/{question['titleSlug']}/

---

## 题目描述

{question['content']}

---

## 代码模板

"""

    for snippet in question.get('codeSnippets', []):
        if snippet['langSlug'] in ['python3', 'java', 'cpp', 'javascript', 'golang']:
            content += f"\n### {snippet['lang']}\n\n```{snippet['langSlug']}\n{snippet['code']}\n```\n"

    if question.get('hints'):
        content += "\n---\n\n## 提示\n\n"
        for i, hint in enumerate(question['hints'], 1):
            content += f"{i}. {hint}\n"

    if question.get('sampleTestCase'):
        content += f"\n---\n\n## 示例测试用例\n\n```\n{question['sampleTestCase']}\n```\n"

    # AI 解答
    if ai_solution:
        content += "\n---\n\n## AI 解答 (DeepSeek)\n\n"
        content += ai_solution + "\n"
    else:
        content += "\n---\n\n## AI 解答\n\n*DeepSeek API 未配置或调用失败*\n"

    content += f"\n---\n\n*获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ 已保存: {filename}")
    return True

class HTMLGenerator:
    """HTML 页面生成器"""
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def convert_markdown_to_html(self, md_files: List[str], date_str: str, time_str: str) -> Optional[str]:
        """将当天的 markdown 文件转换为一个 HTML 页面"""
        if not MARKDOWN2_AVAILABLE:
            print("  ⚠ markdown2 未安装，跳过 HTML 生成")
            return None

        if not md_files:
            return None

        # 读取所有 markdown 文件内容
        all_content = []
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_content.append(content)
            except Exception as e:
                print(f"  ⚠ 读取文件失败 {md_file}: {e}")

        if not all_content:
            return None

        # 合并内容，用分隔线分开
        combined_md = "\n\n---\n\n".join(all_content)

        # 转换为 HTML
        html_body = markdown2.markdown(
            combined_md,
            extras=['fenced-code-blocks', 'tables', 'header-ids']
        )

        # 生成完整 HTML，文件名包含时间戳
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        html_filename = f"{date_str}_{time_str}.html"
        html_file = self.docs_dir / html_filename

        # 格式化时间显示
        formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"

        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LeetCode {formatted_date} {formatted_time}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 返回首页</a>
        <div class="content">
            <h1>📅 {formatted_date} {formatted_time} 每日题目</h1>
            {html_body}
        </div>
    </div>
</body>
</html>"""

        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            print(f"  ✓ 已生成 HTML: {html_file.name}")
            return html_filename
        except Exception as e:
            print(f"  ✗ HTML 生成失败: {e}")
            return None

    def update_index_page(self, date_str: str, time_str: str, html_filename: str, question_count: int, total_questions: int):
        """更新索引页面"""
        index_file = self.docs_dir / "index.html"

        if not index_file.exists():
            print(f"  ⚠ 索引文件不存在: {index_file}")
            return False

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 格式化日期和时间显示
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
            formatted_datetime = f"{formatted_date} {formatted_time}"

            # 构造本次执行的条目
            item = f'''            <div class="day-item latest">
                <span class="date">{formatted_datetime}</span>
                <a href="{html_filename}">查看题目</a>
                <span class="count">共 {question_count} 题</span>
            </div>'''

            # 移除空状态提示（如果存在）
            content = re.sub(
                r'<div class="empty-state">.*?</div>',
                '',
                content,
                flags=re.DOTALL
            )

            # 每次都在列表顶部插入新条目（不检查重复）
            if '<div class="daily-list">' in content:
                content = content.replace(
                    '<div class="daily-list">',
                    f'<div class="daily-list">\n{item}',
                    1
                )

            # 更新时间戳
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            content = re.sub(
                r'<p class="update-time">最后更新：.*?</p>',
                f'<p class="update-time">最后更新：{now}</p>',
                content
            )

            # 更新统计信息
            # 计算天数（有多少个 day-item）
            day_count = content.count('class="day-item')

            content = re.sub(
                r'(<div class="stat-item">[\s\S]*?<span class="stat-label">累计题目</span>[\s\S]*?<span class="stat-value">)\d+(</span>)',
                f'\\g<1>{total_questions}\\g<2>',
                content
            )

            content = re.sub(
                r'(<div class="stat-item">[\s\S]*?<span class="stat-label">连续天数</span>[\s\S]*?<span class="stat-value">)\d+(</span>)',
                f'\\g<1>{day_count}\\g<2>',
                content
            )

            # 保存更新后的内容
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✓ 已更新索引页面")
            return True

        except Exception as e:
            print(f"  ✗ 更新索引页面失败: {e}")
            return False

    def update_history_json(self, date_str: str, time_str: str, html_filename: str, question_count: int):
        """更新历史记录 JSON 文件"""
        history_file = self.docs_dir / "history.json"

        # 格式化日期和时间显示
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
        formatted_datetime = f"{formatted_date} {formatted_time}"

        # 构造新记录
        new_record = {
            "date": formatted_datetime,
            "file": html_filename,
            "count": question_count
        }

        try:
            # 读取现有记录
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    records = data.get('records', [])
            else:
                records = []

            # 在列表开头插入新记录
            records.insert(0, new_record)

            # 保存更新后的记录
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'records': records,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }, f, ensure_ascii=False, indent=2)

            print(f"  ✓ 已更新历史记录")
            return True

        except Exception as e:
            print(f"  ✗ 更新历史记录失败: {e}")
            return False

class GitHubPagesPublisher:
    """GitHub Pages 发布器"""
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', False)
        self.username = config.get('username', '')
        self.repo = config.get('repo', 'leetcode')
        self.site_url = config.get('site_url', '')

    def is_available(self) -> bool:
        """检查是否已配置"""
        if not self.enabled:
            return False
        if not self.username or self.username == 'YOUR_GITHUB_USERNAME':
            return False
        return True

    def check_git_initialized(self) -> bool:
        """检查 Git 是否已初始化"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def git_add_commit_push(self, date_str: str, questions: List[Dict] = None) -> bool:
        """添加、提交并推送到 GitHub"""
        if not self.is_available():
            print("  ⚠ GitHub Pages 未启用或未配置")
            return False

        if not self.check_git_initialized():
            print("  ⚠ Git 仓库未初始化，请先运行 git init")
            print("  提示: 查看 GITHUB_PAGES_SETUP.md 了解详细配置步骤")
            return False

        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        formatted_time = datetime.now().strftime("%H:%M:%S")

        # 生成详细的 commit message
        if questions and len(questions) > 0:
            # 统计难度分布
            difficulty_count = {'Easy': 0, 'Medium': 0, 'Hard': 0}
            question_titles = []

            for q in questions:
                diff = q.get('difficulty', 'Medium')
                difficulty_count[diff] = difficulty_count.get(diff, 0) + 1
                # 获取题号和标题
                q_id = q.get('questionFrontendId', '?')
                q_title = q.get('title', '未知题目')
                question_titles.append(f"{q_id}. {q_title}")

            # 构建 commit message
            difficulty_parts = []
            if difficulty_count['Easy'] > 0:
                difficulty_parts.append(f"{difficulty_count['Easy']}E")
            if difficulty_count['Medium'] > 0:
                difficulty_parts.append(f"{difficulty_count['Medium']}M")
            if difficulty_count['Hard'] > 0:
                difficulty_parts.append(f"{difficulty_count['Hard']}H")

            difficulty_str = "+".join(difficulty_parts) if difficulty_parts else "3题"

            # 主标题
            commit_title = f"📝 {formatted_date} {formatted_time} | {difficulty_str}"

            # 详细信息（换行）
            commit_body = "\n\n".join([f"• {title}" for title in question_titles])

            commit_message = f"{commit_title}\n\n{commit_body}\n\n🤖 Auto-generated by LeetCode Daily Script"
        else:
            # 降级方案：简单的 commit message
            commit_message = f"📝 {formatted_date} {formatted_time} | Add LeetCode questions\n\n🤖 Auto-generated by LeetCode Daily Script"

        commands = [
            ['git', 'add', 'docs/'],
            ['git', 'add', 'leetcode_questions/'],
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
                    # git commit 如果没有变更会返回非 0，这是正常的
                    if 'nothing to commit' in result.stdout or 'nothing to commit' in result.stderr:
                        print(f"  ℹ️  没有需要提交的变更")
                        continue
                    else:
                        print(f"  ✗ 命令失败: {result.stderr}")
                        return False

            print(f"  ✓ 已推送到 GitHub")
            if self.site_url:
                print(f"  🌐 访问: {self.site_url}")
            return True

        except subprocess.TimeoutExpired:
            print(f"  ✗ Git 操作超时")
            return False
        except Exception as e:
            print(f"  ✗ Git 操作失败: {e}")
            return False

def main():
    print("=" * 60)
    print("LeetCode 每日题目获取脚本 (DeepSeek AI 增强版)")
    print("=" * 60)
    print()

    # 加载配置
    config = load_config()
    if not config:
        return

    # 初始化执行日志
    logger = ExecutionLogger("execution.log")

    # 初始化历史记录
    history = QuestionHistory(config['history_file'])
    stats = history.get_stats()
    print(f"历史记录: 已选择 {stats['total_selected']} 道题目")

    # 初始化 DeepSeek API
    deepseek = DeepSeekAPI(config.get('deepseek', {}))
    if deepseek.is_available():
        print(f"DeepSeek API: 已启用 (模型: {deepseek.model})")
    else:
        print(f"DeepSeek API: 未配置或已禁用")

    print()

    # 获取题目列表
    fetcher = LeetCodeFetcher()
    print("正在获取题目列表...")
    all_questions = fetcher.get_all_questions()

    if not all_questions:
        print("❌ 无法获取题目列表")
        return

    print(f"✓ 共获取 {len(all_questions)} 道题目")

    # 按难度选择题目
    selected_questions = select_questions_by_difficulty(
        all_questions,
        config['difficulties'],
        history
    )

    if not selected_questions:
        print("❌ 没有可选的题目（可能都已被选过）")
        return

    print(f"✓ 随机选择 {len(selected_questions)} 道题目")
    print()

    # 获取详情并保存
    saved_count = 0
    saved_files = []  # 记录保存的文件路径
    date_str = datetime.now().strftime("%Y%m%d")

    for i, q in enumerate(selected_questions, 1):
        print(f"[{i}/{len(selected_questions)}] {q['difficulty']} - {q['questionFrontendId']}. {q['title']}")

        # 获取详情
        detail = fetcher.get_question_detail(q['titleSlug'])
        if not detail:
            print(f"  ✗ 跳过（获取失败）")
            logger.add_result(i, False, q['title'])
            continue

        # 获取 AI 解答
        ai_solution = None
        if deepseek.is_available():
            print(f"  正在生成 AI 解答...")
            ai_solution = deepseek.generate_solution(detail)
            if ai_solution:
                print(f"  ✓ AI 解答已生成")

        # 保存 Markdown
        if save_as_markdown(detail, ai_solution, config['output_dir']):
            saved_count += 1
            history.add(q['questionId'])
            logger.add_result(i, True, q['title'])

            # 记录保存的文件
            chinese_title = detail['title']
            chinese_title = re.sub(r'[<>:"/\\|?*]', '', chinese_title).strip()
            difficulty_map = {'Easy': '简单', 'Medium': '中等', 'Hard': '困难'}
            difficulty_cn = difficulty_map.get(detail['difficulty'], detail['difficulty'])
            filename = f"{detail['questionFrontendId']}_{difficulty_cn}_{chinese_title}_{date_str}.md"
            saved_files.append(os.path.join(config['output_dir'], filename))
        else:
            logger.add_result(i, False, q['title'])

        print()

    # 保存执行日志
    logger.save()

    print("=" * 60)
    print(f"完成! 成功保存 {saved_count} 道题目")
    print(f"保存位置: {os.path.abspath(config['output_dir'])}")
    print(f"历史记录: 累计已选择 {len(history.history)} 道题目")
    print("=" * 60)
    print()

    # GitHub Pages 发布
    github_config = config.get('github_pages', {})
    if github_config.get('enabled', False) and saved_files:
        print("正在生成 GitHub Pages...")

        # 获取当前时间戳（时分秒）
        time_str = datetime.now().strftime("%H%M%S")

        # 生成 HTML
        html_gen = HTMLGenerator("docs")
        html_filename = html_gen.convert_markdown_to_html(saved_files, date_str, time_str)

        if html_filename:
            # 更新索引页
            html_gen.update_index_page(date_str, time_str, html_filename, saved_count, len(history.history))

            # 更新历史记录 JSON
            html_gen.update_history_json(date_str, time_str, html_filename, saved_count)

            # 推送到 GitHub
            publisher = GitHubPagesPublisher(github_config)
            if publisher.is_available():
                print()
                print("正在推送到 GitHub...")
                publisher.git_add_commit_push(date_str, selected_questions)
            else:
                print("  ⚠ GitHub Pages 未完全配置，跳过推送")
                print("  提示: 查看 GITHUB_PAGES_SETUP.md 了解配置步骤")

        print()
        print("=" * 60)

    # 发送系统通知
    send_notification("LeetCode Job", "job 执行完毕")

if __name__ == "__main__":
    main()
