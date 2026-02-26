#!/bin/bash
# LeetCode 定时任务卸载脚本

echo "========================================"
echo "LeetCode 每日题目获取 - 定时任务卸载"
echo "========================================"
echo ""

TARGET_PLIST="$HOME/Library/LaunchAgents/com.leetcode.daily.plist"

if [ ! -f "$TARGET_PLIST" ]; then
    echo "未找到定时任务配置文件"
    echo "可能任务未安装或已被删除"
    exit 0
fi

# 卸载任务
echo "正在卸载定时任务..."
launchctl unload "$TARGET_PLIST" 2>/dev/null

# 删除配置文件
rm "$TARGET_PLIST"

if [ $? -eq 0 ]; then
    echo "✓ 定时任务已成功卸载"
else
    echo "错误: 卸载失败"
    exit 1
fi

echo ""
echo "========================================"
echo "卸载完成!"
echo "========================================"
echo ""
echo "注意: 已下载的题目文件未被删除"
echo "如需删除，请手动删除 leetcode_questions 目录"
echo ""
