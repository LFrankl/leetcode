#!/bin/bash
# LeetCode 定时任务安装脚本

echo "========================================"
echo "LeetCode 每日题目获取 - 定时任务安装"
echo "========================================"
echo ""

# 检查 Python3 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3"
    exit 1
fi

echo "✓ Python3 已安装: $(python3 --version)"

# 检查 requests 库
if ! python3 -c "import requests" &> /dev/null; then
    echo "警告: requests 库未安装"
    echo "正在安装 requests..."
    pip3 install requests
    if [ $? -eq 0 ]; then
        echo "✓ requests 库安装成功"
    else
        echo "错误: requests 库安装失败，请手动安装: pip3 install requests"
        exit 1
    fi
else
    echo "✓ requests 库已安装"
fi

echo ""
echo "正在设置定时任务..."

# 获取当前脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$SCRIPT_DIR/com.leetcode.daily.plist"
TARGET_PLIST="$HOME/Library/LaunchAgents/com.leetcode.daily.plist"

# 复制 plist 文件
cp "$PLIST_FILE" "$TARGET_PLIST"
echo "✓ 已复制配置文件到: $TARGET_PLIST"

# 卸载旧任务（如果存在）
launchctl unload "$TARGET_PLIST" 2>/dev/null

# 加载新任务
launchctl load "$TARGET_PLIST"
if [ $? -eq 0 ]; then
    echo "✓ 定时任务已加载成功"
else
    echo "错误: 定时任务加载失败"
    exit 1
fi

echo ""
echo "========================================"
echo "安装完成!"
echo "========================================"
echo ""
echo "定时任务将在每天下午 16:15 自动运行"
echo ""
echo "常用命令:"
echo "  手动运行: python3 $SCRIPT_DIR/leetcode_daily.py"
echo "  立即测试: launchctl start com.leetcode.daily"
echo "  查看状态: launchctl list | grep leetcode"
echo "  查看日志: tail -f $SCRIPT_DIR/logs/output.log"
echo "  停止任务: launchctl unload $TARGET_PLIST"
echo ""
