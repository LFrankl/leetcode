// LeetCode 每日题目 - Google 风格应用（三层结构）

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
