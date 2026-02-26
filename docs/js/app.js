// LeetCode 每日题目 - 分页显示版本

class LeetCodeApp {
    constructor() {
        this.allRecords = [];
        this.currentView = 'list'; // 'list' or 'detail'

        // 分页相关
        this.currentPage = 1;
        this.pageSize = 10;
        this.totalPages = 1;

        // 鸡汤文案库
        this.motivationQuotes = [
            "代码如诗，算法如画。每一道题目都是通往卓越的阶梯。",
            "坚持每天刷题，你与梦想的距离就会越来越近。",
            "算法不会背叛努力，坚持就是胜利。",
            "每一次提交，都是对自己的一次挑战。",
            "编程之路漫长，但每一步都算数。",
            "别怕题目难，怕的是不敢开始。",
            "优秀的程序员都是从一道道题目中成长起来的。",
            "今天解决的 bug，就是明天的经验。",
            "代码改变世界，而你正在改变代码。",
            "保持好奇心，永远在学习的路上。"
        ];

        this.init();
    }

    async init() {
        // 绑定事件
        this.bindEvents();

        // 加载历史数据
        await this.loadHistory();

        // 显示第一页
        this.renderPage();

        // 随机显示鸡汤
        this.showRandomMotivation();
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
            this.showRecordList();
        });

        // FAB 返回按钮
        document.getElementById('fabBack').addEventListener('click', () => {
            this.showRecordList();
        });

        // ESC 键关闭侧边栏
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                this.closeSidebar();
            }
        });

        // 分页控件事件
        document.getElementById('prevPage').addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.renderPage();
            }
        });

        document.getElementById('nextPage').addEventListener('click', () => {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.renderPage();
            }
        });

        document.getElementById('pageInput').addEventListener('change', (e) => {
            const page = parseInt(e.target.value);
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.renderPage();
            } else {
                e.target.value = this.currentPage;
            }
        });

        const pageSizeSelector = document.getElementById('pageSize');
        pageSizeSelector.addEventListener('change', (e) => {
            const oldPageSize = this.pageSize;
            const newPageSize = parseInt(e.target.value);

            console.log(`页面大小改变: ${oldPageSize} → ${newPageSize}`);

            this.pageSize = newPageSize;

            // 重新计算当前页，保持用户看到的第一条记录尽可能不变
            const firstRecordIndex = (this.currentPage - 1) * oldPageSize;
            this.currentPage = Math.floor(firstRecordIndex / this.pageSize) + 1;

            console.log(`当前页重新计算: ${this.currentPage}`);

            this.renderPage();
        });

        // 确保 select 在移动端可点击
        pageSizeSelector.addEventListener('touchstart', (e) => {
            e.stopPropagation();
        });
    }

    closeSidebar() {
        document.getElementById('sidebar').classList.remove('open');
        document.getElementById('sidebarOverlay').classList.remove('visible');
    }

    async loadHistory() {
        try {
            // 添加时间戳防止浏览器缓存
            const response = await fetch(`history.json?t=${Date.now()}`);
            if (!response.ok) {
                throw new Error('无法加载历史记录');
            }

            const data = await response.json();
            this.allRecords = data.records || [];

            // 按时间倒序排序（最新的在前）
            this.allRecords.sort((a, b) => {
                return new Date(b.date) - new Date(a.date);
            });

            // 更新统计
            this.updateStats();

        } catch (error) {
            console.error('加载历史记录失败:', error);
            this.allRecords = [];
        }
    }

    calculatePagination() {
        this.totalPages = Math.ceil(this.allRecords.length / this.pageSize);
        if (this.currentPage > this.totalPages) {
            this.currentPage = this.totalPages || 1;
        }
    }

    renderPage() {
        this.calculatePagination();

        // 更新标题
        document.getElementById('contentTitle').textContent = '所有记录';
        document.getElementById('contentSubtitle').textContent =
            `共 ${this.allRecords.length} 条记录`;

        // 计算当前页的记录
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = Math.min(startIndex + this.pageSize, this.allRecords.length);
        const pageRecords = this.allRecords.slice(startIndex, endIndex);

        // 渲染记录列表
        this.renderRecordList(pageRecords);

        // 更新分页控件
        this.updatePaginationControls();
    }

    updatePaginationControls() {
        // 更新按钮状态
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');

        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= this.totalPages;

        // 更新页码输入框
        document.getElementById('pageInput').value = this.currentPage;
        document.getElementById('pageInput').max = this.totalPages;
        document.getElementById('totalPages').textContent = this.totalPages;
    }

    renderRecordList(records) {
        const recordList = document.getElementById('recordList');

        if (records.length === 0) {
            recordList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📝</div>
                    <div class="empty-state-text">暂无记录</div>
                    <div class="empty-state-hint">运行脚本后，记录将自动显示在这里</div>
                </div>
            `;
            return;
        }

        // 难度中文映射
        const difficultyMap = {
            'easy': '简单',
            'medium': '中等',
            'hard': '困难'
        };

        recordList.innerHTML = records.map((record, index) => {
            // 计算全局索引
            const globalIndex = (this.currentPage - 1) * this.pageSize + index;

            // 生成题目预览列表
            const questionsHTML = record.questions ? record.questions.map(q => {
                // 标题截断（最多30个字符）
                const truncatedTitle = q.title.length > 30
                    ? q.title.substring(0, 30) + '...'
                    : q.title;

                return `
                    <div class="record-question-item">
                        <span class="record-question-bullet">▪</span>
                        <span class="record-question-number">${q.number}.</span>
                        <span class="record-question-title">${truncatedTitle}</span>
                        <span class="record-question-difficulty ${q.difficulty}">
                            ${difficultyMap[q.difficulty] || '未知'}
                        </span>
                    </div>
                `;
            }).join('') : '';

            return `
                <div class="record-card" onclick="app.viewRecord(${globalIndex})">
                    <div class="record-header">
                        <div class="record-time">${record.date}</div>
                        <div class="record-info">共 ${record.count} 道题目</div>
                        <div class="record-arrow">→</div>
                    </div>
                    ${questionsHTML ? `<div class="record-questions">${questionsHTML}</div>` : ''}
                </div>
            `;
        }).join('');
    }

    viewRecord(globalIndex) {
        const record = this.allRecords[globalIndex];
        if (!record) return;

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

    showRecordList() {
        this.currentView = 'list';
        document.getElementById('recordListView').style.display = 'block';
        document.getElementById('questionDetailView').classList.remove('active');

        // 滚动到顶部
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    updateStats() {
        // 更新统计数据
        const totalQuestions = this.allRecords.reduce((sum, record) => sum + record.count, 0);

        // 计算连续天数（按日期去重）
        const uniqueDates = new Set();
        this.allRecords.forEach(record => {
            const dateOnly = record.date.split(' ')[0];
            uniqueDates.add(dateOnly);
        });

        document.getElementById('totalQuestions').textContent = totalQuestions;
        document.getElementById('continuousDays').textContent = uniqueDates.size;

        // 更新最后更新时间
        if (this.allRecords.length > 0) {
            document.getElementById('updateTime').textContent =
                `最后更新：${this.allRecords[0].date}`;
        }
    }

    showRandomMotivation() {
        const randomIndex = Math.floor(Math.random() * this.motivationQuotes.length);
        const motivationText = document.getElementById('motivationText');
        if (motivationText) {
            motivationText.textContent = `"${this.motivationQuotes[randomIndex]}"`;
        }
    }
}

// 初始化应用
const app = new LeetCodeApp();
