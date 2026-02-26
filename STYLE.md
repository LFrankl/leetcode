# UI 设计系统规范

本文档定义了项目的完整 UI 设计系统，基于 Google Material Design 原则，可直接复用到其他项目。

---

## 📋 目录

1. [设计原则](#设计原则)
2. [颜色系统](#颜色系统)
3. [排版系统](#排版系统)
4. [间距系统](#间距系统)
5. [阴影与层级](#阴影与层级)
6. [动画与过渡](#动画与过渡)
7. [组件库](#组件库)
8. [响应式断点](#响应式断点)
9. [完整 CSS 模板](#完整-css-模板)

---

## 设计原则

### 核心理念

1. **极简优雅**
   - 去除不必要的装饰
   - 留白充足，呼吸感强
   - 层次分明，重点突出

2. **一致性**
   - 统一的圆角（8px）
   - 统一的间距体系（8px 倍数）
   - 统一的动画曲线

3. **可用性优先**
   - 清晰的视觉反馈
   - 明显的交互状态
   - 易于理解的布局

4. **性能优化**
   - 使用 CSS 变量便于主题切换
   - 硬件加速的动画（transform/opacity）
   - 避免过度的阴影和滤镜

---

## 颜色系统

### 主色调 (Primary Colors)

```css
:root {
    /* 主色：蓝色系 - 用于主要操作和强调 */
    --primary-blue: #1a73e8;
    --primary-blue-hover: #1557b0;
    --primary-blue-light: #e8f0fe;  /* 用于背景 */

    /* 文本颜色 */
    --text-primary: #202124;        /* 主要文本 */
    --text-secondary: #5f6368;      /* 次要文本、说明 */

    /* 背景颜色 */
    --background: #ffffff;          /* 页面背景 */
    --surface: #f8f9fa;             /* 卡片、面板背景 */

    /* 边框颜色 */
    --border: #dadce0;              /* 分割线、边框 */
}
```

### 语义化颜色

```css
:root {
    /* 成功 - 绿色 */
    --success-bg: #e6f4ea;
    --success-text: #137333;

    /* 警告 - 橙色 */
    --warning-bg: #fef7e0;
    --warning-text: #b06000;

    /* 错误/危险 - 红色 */
    --error-bg: #fce8e6;
    --error-text: #c5221f;

    /* 信息 - 蓝色 */
    --info-bg: #e8f0fe;
    --info-text: #1967d2;
}
```

### 难度颜色（LeetCode 项目专用）

```css
/* 简单 */
.difficulty-easy {
    background: #e6f4ea;
    color: #137333;
}

/* 中等 */
.difficulty-medium {
    background: #fef7e0;
    color: #b06000;
}

/* 困难 */
.difficulty-hard {
    background: #fce8e6;
    color: #c5221f;
}
```

### 颜色使用指南

| 用途 | 颜色变量 | 示例 |
|------|---------|------|
| 主要按钮 | `--primary-blue` | "保存"、"提交" |
| 链接 | `--primary-blue` | 文章链接、导航链接 |
| 标题 | `--text-primary` | H1, H2, H3 |
| 正文 | `--text-primary` | 段落文本 |
| 说明文字 | `--text-secondary` | 提示信息、元数据 |
| 卡片背景 | `--background` | 内容卡片 |
| 页面背景 | `--background` | body 背景 |
| 次要背景 | `--surface` | 侧边栏、工具栏 |

---

## 排版系统

### 字体家族

```css
body {
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 等宽字体（代码、数字） */
code, pre, .monospace {
    font-family: 'SF Mono', Monaco, 'Cascadia Code', Consolas, monospace;
}
```

### 字体大小与粗细

```css
:root {
    /* 字体大小 */
    --text-xs: 11px;     /* 极小文本 */
    --text-sm: 12px;     /* 小文本、标签 */
    --text-base: 13px;   /* 基础文本 */
    --text-md: 14px;     /* 正文 */
    --text-lg: 16px;     /* 小标题 */
    --text-xl: 18px;     /* 二级标题 */
    --text-2xl: 20px;    /* 一级标题 */
    --text-3xl: 24px;    /* 页面标题 */
    --text-4xl: 32px;    /* 大标题 */

    /* 字体粗细 */
    --font-normal: 400;
    --font-medium: 500;
    --font-semibold: 600;
}
```

### 行高

```css
body {
    line-height: 1.6;    /* 正文行高 */
}

/* 标题行高 */
h1, h2, h3, h4, h5, h6 {
    line-height: 1.2;
}
```

### 排版示例

```css
/* 大标题 */
.page-title {
    font-size: 32px;
    font-weight: 400;
    letter-spacing: -0.5px;
    color: var(--text-primary);
}

/* 卡片标题 */
.card-title {
    font-size: 18px;
    font-weight: 500;
    color: var(--text-primary);
}

/* 正文 */
.body-text {
    font-size: 14px;
    font-weight: 400;
    color: var(--text-primary);
    line-height: 1.6;
}

/* 辅助文字 */
.caption {
    font-size: 12px;
    color: var(--text-secondary);
}
```

---

## 间距系统

### 基础单位

使用 **8px 网格系统**，所有间距都是 8 的倍数。

```css
:root {
    --space-xs: 4px;      /* 0.5x */
    --space-sm: 8px;      /* 1x */
    --space-md: 16px;     /* 2x */
    --space-lg: 24px;     /* 3x */
    --space-xl: 32px;     /* 4x */
    --space-2xl: 48px;    /* 6x */
    --space-3xl: 64px;    /* 8x */
}
```

### 间距使用规范

| 用途 | 间距值 | 场景 |
|------|--------|------|
| 元素内边距（小） | 8px | 小按钮、标签 |
| 元素内边距（中） | 16px | 输入框、普通按钮 |
| 元素内边距（大） | 24px | 卡片内容区 |
| 元素间距（紧密） | 4px | 同组元素 |
| 元素间距（正常） | 8px | 列表项、表单字段 |
| 元素间距（宽松） | 16px | 卡片之间 |
| 区块间距 | 32px | 页面区块 |
| 页面内边距 | 24px | 容器 padding |

```css
/* 示例：卡片间距 */
.card-list {
    display: flex;
    flex-direction: column;
    gap: 16px;  /* 卡片之间 16px 间距 */
}

.card {
    padding: 20px 24px;  /* 上下 20px，左右 24px */
}
```

---

## 阴影与层级

### 阴影系统

基于 Material Design 的标准阴影：

```css
:root {
    /* 基础阴影 - 用于卡片、面板 */
    --shadow: 0 1px 2px 0 rgba(60,64,67,0.3),
              0 1px 3px 1px rgba(60,64,67,0.15);

    /* 悬停阴影 - 用于交互元素的 hover 状态 */
    --shadow-hover: 0 1px 3px 0 rgba(60,64,67,0.3),
                    0 4px 8px 3px rgba(60,64,67,0.15);

    /* 浮起阴影 - 用于对话框、弹出菜单 */
    --shadow-raised: 0 2px 4px 0 rgba(60,64,67,0.3),
                     0 4px 8px 3px rgba(60,64,67,0.15);

    /* 深层阴影 - 用于模态框、FAB 按钮 */
    --shadow-deep: 0 4px 8px 0 rgba(60,64,67,0.3),
                   0 8px 16px 6px rgba(60,64,67,0.15);
}
```

### 层级（z-index）

```css
:root {
    --z-dropdown: 1000;      /* 下拉菜单 */
    --z-sticky: 1020;        /* 粘性头部 */
    --z-fixed: 1030;         /* 固定导航 */
    --z-modal-backdrop: 1040;/* 模态背景 */
    --z-modal: 1050;         /* 模态框 */
    --z-popover: 1060;       /* 气泡提示 */
    --z-tooltip: 1070;       /* 工具提示 */
}
```

### 使用示例

```css
/* 基础卡片 */
.card {
    box-shadow: var(--shadow);
}

/* 可交互卡片 */
.card-interactive {
    box-shadow: var(--shadow);
    transition: box-shadow 0.3s;
}

.card-interactive:hover {
    box-shadow: var(--shadow-hover);
}

/* 浮动按钮 */
.fab {
    box-shadow: var(--shadow-deep);
    z-index: 50;
}
```

---

## 动画与过渡

### 缓动曲线

使用 Material Design 标准曲线：

```css
:root {
    /* 标准缓动 - 适用于大多数场景 */
    --ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);

    /* 减速缓动 - 元素进入屏幕 */
    --ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);

    /* 加速缓动 - 元素退出屏幕 */
    --ease-accelerate: cubic-bezier(0.4, 0.0, 1, 1);

    /* 尖锐缓动 - 快速响应 */
    --ease-sharp: cubic-bezier(0.4, 0.0, 0.6, 1);
}
```

### 持续时间

```css
:root {
    --duration-fast: 150ms;      /* 快速反馈 */
    --duration-normal: 200ms;    /* 正常过渡 */
    --duration-slow: 300ms;      /* 舒缓过渡 */
    --duration-slower: 400ms;    /* 大型元素 */
}
```

### 常用动画

#### 1. 淡入淡出

```css
.fade-in {
    animation: fadeIn 300ms var(--ease-decelerate);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.fade-out {
    animation: fadeOut 200ms var(--ease-accelerate);
}

@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}
```

#### 2. 滑入滑出

```css
.slide-in-right {
    animation: slideInRight 300ms var(--ease-decelerate);
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(24px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
```

#### 3. 缩放（悬停效果）

```css
.scale-on-hover {
    transition: all 0.3s var(--ease-standard);
    transform-origin: center;
}

.scale-on-hover:hover {
    transform: scale(1.02);
}
```

#### 4. 旋转加载

```css
.spinner {
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

---

## 组件库

### 1. 按钮

#### 主要按钮

```css
.btn-primary {
    padding: 10px 24px;
    background: var(--primary-blue);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s var(--ease-standard);
}

.btn-primary:hover {
    background: var(--primary-blue-hover);
    box-shadow: var(--shadow);
}

.btn-primary:active {
    transform: scale(0.98);
}
```

#### 次要按钮

```css
.btn-secondary {
    padding: 10px 24px;
    background: transparent;
    color: var(--primary-blue);
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s var(--ease-standard);
}

.btn-secondary:hover {
    background: var(--surface);
    border-color: var(--primary-blue);
}
```

#### 图标按钮

```css
.btn-icon {
    width: 40px;
    height: 40px;
    padding: 0;
    background: transparent;
    border: none;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s var(--ease-standard);
}

.btn-icon:hover {
    background: var(--surface);
}
```

#### 浮动操作按钮 (FAB)

```css
.fab {
    position: fixed;
    bottom: 32px;
    right: 32px;
    width: 56px;
    height: 56px;
    background: var(--primary-blue);
    border: none;
    border-radius: 50%;
    box-shadow: var(--shadow-deep);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    z-index: 50;
    transition: all 0.2s var(--ease-standard);
}

.fab:hover {
    box-shadow: 0 4px 8px 0 rgba(60,64,67,0.3),
                0 8px 16px 6px rgba(60,64,67,0.15);
    transform: scale(1.05);
}

.fab:active {
    transform: scale(0.95);
}
```

### 2. 卡片

#### 基础卡片

```css
.card {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 24px;
    box-shadow: var(--shadow);
}
```

#### 交互式卡片

```css
.card-interactive {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px 24px;
    box-shadow: var(--shadow);
    cursor: pointer;
    transition: all 0.3s var(--ease-standard);
    transform-origin: center;
}

.card-interactive:hover {
    box-shadow: var(--shadow-hover);
    border-color: var(--primary-blue);
    transform: scale(1.02);
    z-index: 1;
}
```

#### 卡片头部

```css
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border);
}

.card-title {
    font-size: 18px;
    font-weight: 500;
    color: var(--text-primary);
}
```

### 3. 徽章 (Badge)

```css
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
}

/* 成功徽章 */
.badge-success {
    background: var(--success-bg);
    color: var(--success-text);
}

/* 警告徽章 */
.badge-warning {
    background: var(--warning-bg);
    color: var(--warning-text);
}

/* 错误徽章 */
.badge-error {
    background: var(--error-bg);
    color: var(--error-text);
}

/* 信息徽章 */
.badge-info {
    background: var(--info-bg);
    color: var(--info-text);
}
```

### 4. 导航栏

```css
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background: var(--background);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 24px;
    z-index: 100;
    box-shadow: 0 1px 2px rgba(60,64,67,0.1);
}

.navbar-brand {
    font-size: 20px;
    font-weight: 400;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}
```

### 5. 侧边栏

```css
.sidebar {
    position: fixed;
    top: 64px;  /* 导航栏高度 */
    left: 0;
    width: 280px;
    height: calc(100vh - 64px);
    background: var(--background);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    z-index: 99;
}

/* 侧边栏头部 */
.sidebar-header {
    padding: 24px;
    border-bottom: 1px solid var(--border);
}

/* 侧边栏列表项 */
.sidebar-item {
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.2s var(--ease-standard);
    border-left: 3px solid transparent;
}

.sidebar-item:hover {
    background: var(--surface);
}

.sidebar-item.active {
    background: var(--info-bg);
    border-left-color: var(--primary-blue);
}
```

### 6. 输入框

```css
.input {
    width: 100%;
    padding: 12px 16px;
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 14px;
    color: var(--text-primary);
    transition: all 0.2s var(--ease-standard);
}

.input:focus {
    outline: none;
    border-color: var(--primary-blue);
    box-shadow: 0 0 0 3px var(--info-bg);
}

.input:disabled {
    background: var(--surface);
    cursor: not-allowed;
    opacity: 0.6;
}
```

### 7. 加载状态

```css
.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border);
    border-top-color: var(--primary-blue);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

### 8. 空状态

```css
.empty-state {
    text-align: center;
    padding: 80px 20px;
    color: var(--text-secondary);
}

.empty-state-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.3;
}

.empty-state-text {
    font-size: 16px;
    color: var(--text-secondary);
}

.empty-state-hint {
    font-size: 14px;
    color: var(--text-secondary);
    opacity: 0.7;
    margin-top: 8px;
}
```

---

## 响应式断点

### 断点定义

```css
/* 移动端 */
@media (max-width: 768px) {
    /* 小屏幕样式 */
}

/* 平板 */
@media (min-width: 769px) and (max-width: 1024px) {
    /* 中等屏幕样式 */
}

/* 桌面端 */
@media (min-width: 1025px) {
    /* 大屏幕样式 */
}
```

### 响应式容器

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

@media (max-width: 768px) {
    .container {
        padding: 0 16px;
    }
}
```

### 响应式侧边栏

```css
/* 桌面端：始终显示 */
@media (min-width: 769px) {
    .sidebar {
        left: 0;
    }

    .main-content {
        margin-left: 280px;
    }
}

/* 移动端：默认隐藏 */
@media (max-width: 768px) {
    .sidebar {
        left: -280px;
        transition: left 0.3s var(--ease-standard);
    }

    .sidebar.open {
        left: 0;
    }

    .main-content {
        margin-left: 0;
    }
}
```

---

## 完整 CSS 模板

以下是一个完整的、可直接复用的 CSS 模板：

```css
/* ==================== 基础重置 ==================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ==================== CSS 变量定义 ==================== */
:root {
    /* 主色 */
    --primary-blue: #1a73e8;
    --primary-blue-hover: #1557b0;
    --primary-blue-light: #e8f0fe;

    /* 文本 */
    --text-primary: #202124;
    --text-secondary: #5f6368;

    /* 背景 */
    --background: #ffffff;
    --surface: #f8f9fa;

    /* 边框 */
    --border: #dadce0;

    /* 语义颜色 */
    --success-bg: #e6f4ea;
    --success-text: #137333;
    --warning-bg: #fef7e0;
    --warning-text: #b06000;
    --error-bg: #fce8e6;
    --error-text: #c5221f;
    --info-bg: #e8f0fe;
    --info-text: #1967d2;

    /* 阴影 */
    --shadow: 0 1px 2px 0 rgba(60,64,67,0.3),
              0 1px 3px 1px rgba(60,64,67,0.15);
    --shadow-hover: 0 1px 3px 0 rgba(60,64,67,0.3),
                    0 4px 8px 3px rgba(60,64,67,0.15);
    --shadow-raised: 0 2px 4px 0 rgba(60,64,67,0.3),
                     0 4px 8px 3px rgba(60,64,67,0.15);
    --shadow-deep: 0 4px 8px 0 rgba(60,64,67,0.3),
                   0 8px 16px 6px rgba(60,64,67,0.15);

    /* 间距 */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    --space-2xl: 48px;
    --space-3xl: 64px;

    /* 动画 */
    --ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
    --ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);
    --ease-accelerate: cubic-bezier(0.4, 0.0, 1, 1);

    --duration-fast: 150ms;
    --duration-normal: 200ms;
    --duration-slow: 300ms;
}

/* ==================== 全局样式 ==================== */
body {
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background: var(--background);
    overflow-x: hidden;
}

/* ==================== 按钮组件 ==================== */
.btn {
    padding: 10px 24px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--duration-normal) var(--ease-standard);
    border: none;
    outline: none;
}

.btn-primary {
    background: var(--primary-blue);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-blue-hover);
    box-shadow: var(--shadow);
}

.btn-secondary {
    background: transparent;
    color: var(--primary-blue);
    border: 1px solid var(--border);
}

.btn-secondary:hover {
    background: var(--surface);
    border-color: var(--primary-blue);
}

/* ==================== 卡片组件 ==================== */
.card {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: var(--space-lg);
    box-shadow: var(--shadow);
}

.card-interactive {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: var(--space-lg);
    box-shadow: var(--shadow);
    cursor: pointer;
    transition: all var(--duration-slow) var(--ease-standard);
    transform-origin: center;
}

.card-interactive:hover {
    box-shadow: var(--shadow-hover);
    border-color: var(--primary-blue);
    transform: scale(1.02);
    z-index: 1;
}

/* ==================== 徽章组件 ==================== */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.badge-success {
    background: var(--success-bg);
    color: var(--success-text);
}

.badge-warning {
    background: var(--warning-bg);
    color: var(--warning-text);
}

.badge-error {
    background: var(--error-bg);
    color: var(--error-text);
}

/* ==================== 导航栏 ==================== */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background: var(--background);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 var(--space-lg);
    z-index: 100;
}

/* ==================== 侧边栏 ==================== */
.sidebar {
    position: fixed;
    top: 64px;
    left: 0;
    width: 280px;
    height: calc(100vh - 64px);
    background: var(--background);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    z-index: 99;
}

/* ==================== 工具类 ==================== */
.text-primary { color: var(--text-primary); }
.text-secondary { color: var(--text-secondary); }
.bg-surface { background: var(--surface); }

.p-sm { padding: var(--space-sm); }
.p-md { padding: var(--space-md); }
.p-lg { padding: var(--space-lg); }

.m-sm { margin: var(--space-sm); }
.m-md { margin: var(--space-md); }
.m-lg { margin: var(--space-lg); }

.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.gap-sm { gap: var(--space-sm); }
.gap-md { gap: var(--space-md); }
.gap-lg { gap: var(--space-lg); }

/* ==================== 响应式 ==================== */
@media (max-width: 768px) {
    .sidebar {
        left: -280px;
        transition: left var(--duration-slow) var(--ease-standard);
    }

    .sidebar.open {
        left: 0;
    }
}
```

---

## 使用指南

### 快速开始

1. **复制完整 CSS 模板**到你的项目
2. **根据项目需求调整颜色**（修改 CSS 变量）
3. **使用预定义的组件类**构建界面
4. **必要时扩展组件库**

### 命名规范

- 使用 **BEM 命名法**：`.block__element--modifier`
- 组件类名：`.card`, `.btn`, `.badge`
- 状态类名：`.is-active`, `.is-disabled`, `.is-loading`
- 工具类名：`.flex`, `.p-lg`, `.text-primary`

### 最佳实践

1. **优先使用 CSS 变量**，便于主题切换
2. **使用 transform 和 opacity 做动画**，性能更好
3. **避免过度使用阴影**，影响性能
4. **移动端优先**设计响应式
5. **保持一致的间距**，使用 8px 网格系统

---

## 扩展建议

### 暗黑模式支持

```css
@media (prefers-color-scheme: dark) {
    :root {
        --background: #121212;
        --surface: #1e1e1e;
        --text-primary: #ffffff;
        --text-secondary: #aaaaaa;
        --border: #333333;
    }
}
```

### 自定义主题

```css
/* 绿色主题 */
.theme-green {
    --primary-blue: #0f9d58;
    --primary-blue-hover: #0a7e45;
}

/* 紫色主题 */
.theme-purple {
    --primary-blue: #9c27b0;
    --primary-blue-hover: #7b1fa2;
}
```

---

## 参考资源

- [Material Design 官方文档](https://material.io/design)
- [Google Fonts](https://fonts.google.com/)
- [CSS Easing Functions](https://easings.net/)
- [8-Point Grid System](https://spec.fm/specifics/8-pt-grid)

---

**最后更新**: 2026-02-26
**版本**: 1.0
**作者**: Claude (Anthropic)
**许可**: MIT

---

## 附录：完整组件示例

### 示例 1：个人资料卡片

```html
<div class="card">
    <div class="card-header">
        <div class="flex items-center gap-md">
            <img src="avatar.jpg" class="avatar" width="48" height="48">
            <div>
                <h3 class="card-title">张三</h3>
                <p class="text-secondary">软件工程师</p>
            </div>
        </div>
        <span class="badge badge-success">在线</span>
    </div>
    <div class="card-body">
        <p class="text-secondary">热爱编程，专注前端开发</p>
    </div>
</div>
```

### 示例 2：操作卡片列表

```html
<div class="card-list">
    <div class="card-interactive">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-md">
                <span class="icon">📝</span>
                <div>
                    <h4>编辑个人资料</h4>
                    <p class="text-secondary">更新您的个人信息</p>
                </div>
            </div>
            <span class="arrow">→</span>
        </div>
    </div>

    <div class="card-interactive">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-md">
                <span class="icon">🔒</span>
                <div>
                    <h4>修改密码</h4>
                    <p class="text-secondary">保护您的账户安全</p>
                </div>
            </div>
            <span class="arrow">→</span>
        </div>
    </div>
</div>
```

### 示例 3：统计仪表板

```html
<div class="stats-grid">
    <div class="stat-card card">
        <div class="stat-label text-secondary">总用户数</div>
        <div class="stat-value">1,234</div>
        <div class="stat-change">
            <span class="badge badge-success">↑ 12%</span>
        </div>
    </div>

    <div class="stat-card card">
        <div class="stat-label text-secondary">活跃用户</div>
        <div class="stat-value">856</div>
        <div class="stat-change">
            <span class="badge badge-warning">↓ 3%</span>
        </div>
    </div>
</div>

<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: var(--space-md);
}

.stat-value {
    font-size: 36px;
    font-weight: 400;
    color: var(--primary-blue);
    margin: 8px 0;
}
</style>
```

---

**祝你的项目设计得既美观又优雅！** ✨
