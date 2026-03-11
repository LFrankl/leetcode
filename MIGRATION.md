# 迁移指南：在新机器上重建服务

本文档说明如何从 GitHub 仓库克隆项目，并在各平台上重新启动每日定时抓题服务。

---

## 前置条件

- Python 3.8+
- Git
- DeepSeek API Key（[申请地址](https://platform.deepseek.com/)）
- GitHub Personal Access Token，需要 `repo` 权限（[申请地址](https://github.com/settings/tokens)）

---

## 第一步：克隆仓库

```bash
git clone https://github.com/LFrankl/leetcode.git leetcodejob
cd leetcodejob
```

---

## 第二步：安装 Python 依赖

```bash
pip3 install requests markdown2
```

---

## 第三步：创建 config.json

仓库中不包含 `config.json`（含敏感信息，已 gitignore）。参考以下模板创建：

```bash
cp config.example.json config.json
```

然后编辑 `config.json`，填入你的真实信息：

```json
{
  "questions_per_day": 3,
  "difficulties": {
    "easy": 1,
    "medium": 1,
    "hard": 1
  },
  "output_dir": "leetcode_questions",
  "history_file": "question_history.json",
  "language": "zh-CN",
  "github_pages": {
    "enabled": true,
    "username": "你的GitHub用户名",
    "repo": "leetcode",
    "site_url": "https://你的GitHub用户名.github.io/leetcode/"
  },
  "deepseek": {
    "enabled": true,
    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "timeout": 180,
    "max_retries": 3,
    "prompt_template": "..."
  }
}
```

> `prompt_template` 字段直接从 `config.example.json` 复制即可，无需修改。

---

## 第四步：创建必要目录和文件

```bash
mkdir -p logs
touch execution.log
```

`question_history.json` 会在首次运行时自动创建，无需手动建。

---

## 第五步：配置 Git 推送凭证

```bash
git config --global credential.helper store
```

首次执行脚本推送时会提示输入：
- Username：你的 GitHub 用户名
- Password：你的 Personal Access Token（`ghp_xxxxxxxx`）

之后凭证会保存在 `~/.git-credentials`，不再需要重复输入。

---

## 第六步：测试运行

```bash
python3 leetcode_daily.py
```

确认输出正常、题目文件生成、HTML 推送成功后，再配置定时任务。

---

## 第七步：配置定时任务（按平台选择）

### macOS（launchd）

**1. 修改 plist 中的路径**

plist 文件里的路径是硬编码的，需要根据当前机器修改：

```bash
# 查找 Python3 路径
which python3

# 查找项目绝对路径
pwd
```

编辑 `com.leetcode.daily.plist`，替换以下两处：

```xml
<!-- 替换为 which python3 的输出 -->
<string>/Library/Frameworks/Python.framework/Versions/3.11/bin/python3</string>

<!-- 替换为项目实际路径 -->
<string>/Users/你的用户名/路径/leetcodejob/leetcode_daily.py</string>

<!-- WorkingDirectory 同样替换 -->
<string>/Users/你的用户名/路径/leetcodejob</string>

<!-- 日志路径同样替换（两处） -->
<string>/Users/你的用户名/路径/leetcodejob/logs/output.log</string>
<string>/Users/你的用户名/路径/leetcodejob/logs/error.log</string>
```

**2. 安装定时任务**

```bash
./install.sh
```

**3. 验证**

```bash
launchctl list | grep leetcode
# 输出类似：- 0 com.leetcode.daily 表示已注册
```

**默认执行时间**：每天 16:15。修改时间需编辑 plist 中的 `Hour` 和 `Minute`，然后重新加载：

```bash
./reload.sh
```

---

### Linux（systemd）

**1. 创建 service 文件**

```bash
sudo nano /etc/systemd/system/leetcode-daily.service
```

填入以下内容（替换路径和用户名）：

```ini
[Unit]
Description=LeetCode Daily Question Fetcher
After=network.target

[Service]
Type=oneshot
User=你的用户名
WorkingDirectory=/home/你的用户名/路径/leetcodejob
ExecStart=/usr/bin/python3 /home/你的用户名/路径/leetcodejob/leetcode_daily.py
StandardOutput=append:/home/你的用户名/路径/leetcodejob/logs/output.log
StandardError=append:/home/你的用户名/路径/leetcodejob/logs/error.log

[Install]
WantedBy=multi-user.target
```

**2. 创建 timer 文件**

```bash
sudo nano /etc/systemd/system/leetcode-daily.timer
```

```ini
[Unit]
Description=Run LeetCode Daily at 16:15
Requires=leetcode-daily.service

[Timer]
OnCalendar=*-*-* 16:15:00
Persistent=true

[Install]
WantedBy=timers.target
```

**3. 启用并启动**

```bash
sudo systemctl daemon-reload
sudo systemctl enable leetcode-daily.timer
sudo systemctl start leetcode-daily.timer
```

**4. 验证**

```bash
systemctl status leetcode-daily.timer
systemctl list-timers | grep leetcode
```

**手动触发测试：**

```bash
sudo systemctl start leetcode-daily.service
```

---

### Linux（cron，备选方案）

如果不使用 systemd，也可以用 cron：

```bash
crontab -e
```

添加以下行（替换路径）：

```
15 16 * * * cd /home/你的用户名/路径/leetcodejob && python3 leetcode_daily.py >> logs/output.log 2>> logs/error.log
```

---

### Windows（任务计划程序）

**1. 打开任务计划程序**

按 `Win + R`，输入 `taskschd.msc`，回车。

**2. 创建基本任务**

- 点击右侧「创建基本任务」
- 名称：`LeetCode Daily`
- 触发器：每天
- 开始时间：16:15
- 操作：启动程序

**3. 配置程序**

- 程序：`C:\Python311\python.exe`（替换为实际 Python 路径，用 `where python` 查找）
- 参数：`leetcode_daily.py`
- 起始于（工作目录）：`C:\path\to\leetcodejob`

**4. 验证**

在任务计划程序库中找到 `LeetCode Daily`，右键 → 运行，检查是否正常执行。

---

## 常见问题

**Q：脚本找不到 config.json？**

确认 `config.json` 存在于项目根目录，且工作目录（`WorkingDirectory`）配置正确。

**Q：Git push 失败？**

重新配置凭证：

```bash
rm ~/.git-credentials
git config --global credential.helper store
# 再次运行脚本，按提示输入用户名和 Token
```

**Q：DeepSeek API 超时？**

在 `config.json` 中调大 `timeout`（单位：秒）：

```json
"timeout": 300
```

**Q：Linux 下 systemd timer 没触发？**

检查时区是否与预期一致：

```bash
timedatectl status
# 如需修改
sudo timedatectl set-timezone Asia/Shanghai
```

---

## 迁移检查清单

- [ ] 克隆仓库
- [ ] 安装 Python 依赖（`requests`、`markdown2`）
- [ ] 创建 `config.json` 并填入 API Key 和 GitHub 信息
- [ ] 创建 `logs/` 目录
- [ ] 配置 Git 推送凭证
- [ ] 手动运行脚本，确认正常
- [ ] 按平台配置定时任务
- [ ] 验证定时任务状态
