#!/bin/bash
# 重新加载定时任务

echo "========================================"
echo "重新加载 LeetCode 定时任务"
echo "========================================"
echo ""

TARGET_PLIST="$HOME/Library/LaunchAgents/com.leetcode.daily.plist"

# 1. 卸载旧任务
echo "1. 卸载旧任务..."
launchctl unload "$TARGET_PLIST" 2>/dev/null
echo "   ✓ 完成"

# 2. 复制新配置
echo "2. 更新配置文件..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp "$SCRIPT_DIR/com.leetcode.daily.plist" "$TARGET_PLIST"
echo "   ✓ 完成"

# 3. 加载新任务
echo "3. 加载新任务..."
launchctl load "$TARGET_PLIST"
if [ $? -eq 0 ]; then
    echo "   ✓ 完成"
else
    echo "   ✗ 失败"
    exit 1
fi

echo ""
echo "========================================"
echo "重新加载成功！"
echo "========================================"
echo ""
echo "测试命令："
echo "  launchctl start com.leetcode.daily"
echo ""
echo "查看日志："
echo "  tail -f logs/output.log"
echo "  tail -f logs/error.log"
echo ""
