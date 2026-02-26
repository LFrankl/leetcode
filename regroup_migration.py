#!/usr/bin/env python3
"""
重新分组迁移脚本
将 leetcode_questions/ 下的28个 markdown 文件按每4题一组重新生成 HTML
"""

import os
import json
import subprocess
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


def scan_markdown_files(questions_dir):
    """扫描所有 markdown 文件并按日期分组"""
    files_by_date = defaultdict(list)

    md_files = list(Path(questions_dir).glob("*.md"))
    print(f"发现 {len(md_files)} 个 markdown 文件")

    for md_file in md_files:
        # 从文件名提取日期：题号_难度_标题_日期.md
        filename = md_file.stem
        parts = filename.split('_')

        if len(parts) >= 4:
            date_str = parts[-1]  # 最后一部分是日期
            if len(date_str) == 8 and date_str.isdigit():
                files_by_date[date_str].append(str(md_file))

    return files_by_date


def convert_group_to_html(md_files, date_str, time_str, group_num, docs_dir):
    """将一组 markdown 文件转换为一个 HTML 文件"""
    if not md_files:
        return None

    # 读取所有 markdown 文件
    all_content = []
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                all_content.append(content)
        except Exception as e:
            print(f"  ⚠️ 读取失败 {md_file}: {e}")

    if not all_content:
        return None

    # 合并内容
    combined_md = "\n\n---\n\n".join(all_content)

    # 转换为 HTML
    html_body = markdown2.markdown(
        combined_md,
        extras=['fenced-code-blocks', 'tables', 'header-ids']
    )

    # 生成 HTML 文件
    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
    html_filename = f"{date_str}_{time_str}.html"
    html_file = docs_dir / html_filename

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
            <h1>📅 {formatted_date} {formatted_time} 每日题目 (第 {group_num} 组)</h1>
            {html_body}
        </div>
    </div>
</body>
</html>"""

    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        return html_filename
    except Exception as e:
        print(f"  ✗ HTML 生成失败: {e}")
        return None


def update_history_json(records, docs_dir):
    """更新 history.json 文件"""
    history_file = docs_dir / "history.json"

    try:
        # 读取现有记录
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing_records = data.get('records', [])
        else:
            existing_records = []

        # 删除旧的迁移记录（时间为 00:00:00 的记录）
        filtered_records = [
            r for r in existing_records
            if not r['date'].endswith('00:00:00')
        ]

        # 合并新记录（新记录在前）
        all_records = records + filtered_records

        # 去重（基于 file 字段）
        seen_files = set()
        unique_records = []
        for record in all_records:
            if record['file'] not in seen_files:
                seen_files.add(record['file'])
                unique_records.append(record)

        # 按日期时间排序（最新的在前）
        unique_records.sort(key=lambda x: x['date'], reverse=True)

        # 保存
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'records': unique_records,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)

        print(f"✓ 已更新 history.json，共 {len(unique_records)} 条记录")
        return True

    except Exception as e:
        print(f"✗ 更新 history.json 失败: {e}")
        return False


def delete_old_migration_html(docs_dir):
    """删除旧的迁移 HTML 文件（20260226_000000.html）"""
    old_file = docs_dir / "20260226_000000.html"
    if old_file.exists():
        try:
            old_file.unlink()
            print(f"✓ 已删除旧文件: {old_file.name}")
            return True
        except Exception as e:
            print(f"⚠️ 删除旧文件失败: {e}")
            return False
    return True


def git_push(total_groups=0, total_questions=0):
    """提交并推送到 GitHub"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if total_groups > 0:
        commit_message = f"📂 重新分组 | {total_groups} 组 · {total_questions} 道题目\n\n重组时间: {timestamp}\n每组: 4题\n\n🤖 Regrouped by regroup_migration.py"
    else:
        commit_message = f"📂 重新分组\n\n重组时间: {timestamp}\n\n🤖 Regrouped by regroup_migration.py"

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
    print("LeetCode 重新分组迁移脚本")
    print("将28题按每4题一组重新生成 HTML")
    print("=" * 60)
    print()

    # 配置
    questions_dir = Path("leetcode_questions")
    docs_dir = Path("docs")

    if not questions_dir.exists():
        print("❌ leetcode_questions 目录不存在")
        return

    docs_dir.mkdir(parents=True, exist_ok=True)

    # 1. 扫描现有文件
    print("步骤 1: 扫描现有 markdown 文件...")
    files_by_date = scan_markdown_files(questions_dir)

    if not files_by_date:
        print("没有找到需要迁移的文件")
        return

    print(f"找到 {len(files_by_date)} 个不同日期的文件")
    print()

    # 2. 删除旧的迁移文件
    print("步骤 2: 删除旧的迁移文件...")
    delete_old_migration_html(docs_dir)
    print()

    # 3. 按4题一组转换为 HTML
    print("步骤 3: 按4题一组转换为 HTML...")
    new_records = []

    # 按日期排序（从旧到新）
    sorted_dates = sorted(files_by_date.keys())

    for date_str in sorted_dates:
        md_files = sorted(files_by_date[date_str])  # 排序保证顺序一致
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

        print(f"\n处理 {formatted_date} ({len(md_files)} 个文件)")

        # 每4个文件一组
        group_size = 4
        total_groups = (len(md_files) + group_size - 1) // group_size

        for i in range(0, len(md_files), group_size):
            group_files = md_files[i:i+group_size]
            group_num = i // group_size + 1

            # 为每组生成不同的时间戳（每组间隔1小时）
            hour = i // group_size
            time_str = f"{hour:02d}0000"  # 00:00:00, 01:00:00, 02:00:00...

            html_filename = convert_group_to_html(
                group_files,
                date_str,
                time_str,
                group_num,
                docs_dir
            )

            if html_filename:
                formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
                print(f"  ✓ 第 {group_num}/{total_groups} 组: {html_filename} ({len(group_files)} 题)")

                # 添加到记录
                new_records.append({
                    'date': f"{formatted_date} {formatted_time}",
                    'file': html_filename,
                    'count': len(group_files)
                })
            else:
                print(f"  ✗ 第 {group_num} 组生成失败")

    print()
    print(f"成功转换 {len(new_records)} 组文件")
    print()

    # 4. 更新 history.json
    print("步骤 4: 更新 history.json...")
    update_history_json(new_records, docs_dir)
    print()

    # 5. 推送到 GitHub
    print("步骤 5: 推送到 GitHub...")

    # 计算统计信息
    total_questions = sum(r['count'] for r in new_records)

    # 检查是否启用了 GitHub Pages
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            github_enabled = config.get('github_pages', {}).get('enabled', False)
    except:
        github_enabled = False

    if github_enabled:
        git_push(len(new_records), total_questions)
    else:
        print("  ⚠️  GitHub Pages 未启用，跳过推送")
        print("  提示: 如需推送，请在 config.json 中启用 github_pages")

    print()
    print("=" * 60)
    print("重新分组完成！")
    print("=" * 60)
    print()
    print("生成的文件:")
    for record in new_records:
        print(f"  • {record['date']} - {record['file']} ({record['count']} 题)")
    print()
    print("你可以打开 docs/index.html 查看效果")
    print()


if __name__ == "__main__":
    main()
