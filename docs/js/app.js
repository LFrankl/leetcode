// LeetCode 每日题目 - Google 风格应用

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

    async viewRecord(index, date) {
        const records = this.recordsByDate[date];
        const record = records[index];

        // 切换到详情视图
        this.currentView = 'detail';
        document.getElementById('recordListView').style.display = 'none';
        document.getElementById('questionDetailView').classList.add('active');

        // 更新标题
        document.getElementById('detailTitle').textContent = record.date;
        document.getElementById('detailSubtitle').textContent = `共 ${record.count} 题`;

        // 加载题目内容
        await this.loadQuestions(record.file, record.count);

        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    async loadQuestions(file, count) {
        const questionList = document.getElementById('questionList');

        // 显示加载状态
        questionList.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <div>正在加载题目...</div>
            </div>
        `;

        try {
            const response = await fetch(file);
            if (!response.ok) {
                throw new Error('加载失败');
            }

            const html = await response.text();

            // 解析 HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const content = doc.querySelector('.content');

            if (!content) {
                throw new Error('内容格式错误');
            }

            // 提取所有题目（通过 hr 分隔）
            const contentHTML = content.innerHTML;
            const questions = contentHTML.split('<hr>').filter(q => q.trim());

            questionList.innerHTML = questions.map((questionHTML, index) => {
                return this.renderQuestion(questionHTML, index);
            }).join('');

        } catch (error) {
            console.error('加载题目失败:', error);
            questionList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">❌</div>
                    <div class="empty-state-text">加载失败</div>
                    <div class="empty-state-hint">${error.message}</div>
                </div>
            `;
        }
    }

    renderQuestion(questionHTML, index) {
        // 解析题目 HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(questionHTML, 'text/html');

        // 提取题目信息
        const firstH1 = doc.querySelector('h1');
        let questionNumber = '';
        let questionTitle = '';
        let difficulty = '';
        let leetcodeUrl = '';

        if (firstH1) {
            const text = firstH1.textContent;
            const match = text.match(/^(\d+)\.\s*(.+)/);
            if (match) {
                questionNumber = match[1];
                questionTitle = match[2];
            }
        }

        // 提取难度
        const allPs = Array.from(doc.querySelectorAll('p'));
        const difficultyP = allPs.find(p => p.textContent.includes('难度'));
        if (difficultyP) {
            const text = difficultyP.textContent;
            if (text.includes('Easy') || text.includes('简单')) {
                difficulty = 'easy';
            } else if (text.includes('Medium') || text.includes('中等')) {
                difficulty = 'medium';
            } else if (text.includes('Hard') || text.includes('困难')) {
                difficulty = 'hard';
            }
        }

        // 提取 LeetCode 链接
        const linkP = allPs.find(p => p.textContent.includes('链接'));
        if (linkP) {
            const link = linkP.querySelector('a');
            if (link) {
                leetcodeUrl = link.href;
            }
        }

        // 难度中文映射
        const difficultyMap = {
            'easy': '简单',
            'medium': '中等',
            'hard': '困难'
        };

        // 构建题目卡片
        return `
            <div class="question-card">
                <div class="question-header">
                    <span class="question-number">${questionNumber}. ${questionTitle}</span>
                    <span class="difficulty-badge difficulty-${difficulty}">
                        ${difficultyMap[difficulty] || '未知'}
                    </span>
                    ${leetcodeUrl ? `<a href="${leetcodeUrl}" target="_blank" class="question-link">在 LeetCode 打开</a>` : ''}
                </div>
                <div class="markdown-content">
                    ${doc.body.innerHTML}
                </div>
            </div>
        `;
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
