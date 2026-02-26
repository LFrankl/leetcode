#!/bin/bash
# GitHub Pages 快速配置脚本

GITHUB_USERNAME="LFrankl"
REPO_NAME="leetcode"

echo "========================================"
echo "GitHub Pages 配置向导"
echo "========================================"
echo ""
echo "GitHub 用户名: $GITHUB_USERNAME"
echo "仓库名称: $REPO_NAME"
echo ""

# 检查 Git 是否已安装
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

echo "✓ Git 已安装: $(git --version)"
echo ""

# 获取当前目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查是否已经是 Git 仓库
if [ -d ".git" ]; then
    echo "⚠️  检测到已存在 Git 仓库"
    read -p "是否重新初始化？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "保持现有配置"
    else
        echo "正在重新配置..."
        git remote remove origin 2>/dev/null
    fi
else
    echo "正在初始化 Git 仓库..."
    git init
    git branch -M main
    echo "✓ Git 仓库初始化完成"
fi

echo ""

# 添加远程仓库
echo "正在添加远程仓库..."
REMOTE_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

if git remote get-url origin &> /dev/null; then
    echo "远程仓库已存在，更新为: $REMOTE_URL"
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
    echo "✓ 已添加远程仓库: $REMOTE_URL"
fi

echo ""

# 配置 Git 凭证存储
echo "正在配置 Git 凭证存储..."
git config --global credential.helper store
echo "✓ 凭证存储已启用"

echo ""
echo "========================================"
echo "配置完成！"
echo "========================================"
echo ""
echo "接下来的步骤："
echo ""
echo "1. 创建 GitHub 仓库（如果还没创建）："
echo "   访问: https://github.com/new"
echo "   - 仓库名称: $REPO_NAME"
echo "   - 设置为 Public（公开）"
echo "   - 不要勾选 'Add a README file'"
echo ""
echo "2. 创建 Personal Access Token："
echo "   访问: https://github.com/settings/tokens"
echo "   - 点击 'Generate new token (classic)'"
echo "   - 勾选权限: repo"
echo "   - 复制生成的 Token (ghp_xxxx)"
echo ""
echo "3. 安装 Python 依赖："
echo "   pip3 install markdown2"
echo ""
echo "4. 测试运行脚本："
echo "   python3 leetcode_daily.py"
echo ""
echo "   首次运行会提示输入："
echo "   - Username: $GITHUB_USERNAME"
echo "   - Password: 你的 Personal Access Token"
echo ""
echo "5. 启用 GitHub Pages："
echo "   访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main"
echo "   - Folder: /docs"
echo "   - 点击 Save"
echo ""
echo "6. 等待 1-2 分钟后访问你的网站："
echo "   https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo ""
echo "提示: 详细步骤请查看 GITHUB_PAGES_SETUP.md"
echo ""
