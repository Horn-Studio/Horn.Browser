import sys
import os
import webbrowser
import json
from datetime import datetime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile

# 全局样式表
APP_STYLESHEET = """
/* 全局样式 */
QWidget {
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    font-size: 12px;
}

/* 主窗口样式 */
QMainWindow {
    background-color: #f5f7f9;
}

/* 标签页样式 */
QTabWidget::pane {
    border: none;
    background: white;
    border-radius: 0px;
}

QTabBar::tab {
    background: #f0f2f5;
    border: 1px solid #dee2e6;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 15px;
    margin-right: 2px;
    min-width: 120px;
    color: #495057;
}

QTabBar::tab:selected {
    background: white;
    border-color: #dee2e6;
    color: #0d6efd;
    font-weight: bold;
}

QTabBar::tab:!selected {
    background: #e9ecef;
}

QTabBar::close-button {
    subcontrol-position: right;
    subcontrol-origin: padding;
    padding: 2px;
    image: url(icons/close.png);
}

QTabBar::close-button:hover {
    background: #ff6b6b;
    border-radius: 8px;
}

/* 工具栏样式 */
QToolBar {
    background: white;
    border-top: 1px solid #dee2e6;
    padding: 6px;
    spacing: 8px;
}

QToolButton {
    background: transparent;
    border-radius: 8px;
    padding: 6px;
}

QToolButton:hover {
    background: #e9ecef;
}

QToolButton:pressed {
    background: #dee2e6;
}

/* 地址栏样式 */
QLineEdit {
    background: white;
    border: 1px solid #ced4da;
    border-radius: 20px;
    padding: 8px 15px;
    font-size: 14px;
    height: 36px;
}

QLineEdit:focus {
    border-color: #86b7fe;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* 按钮样式 */
QPushButton {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 6px 12px;
    color: #495057;
}

QPushButton:hover {
    background: #e9ecef;
    border-color: #ced4da;
}

QPushButton:pressed {
    background: #dee2e6;
}

/* 对话框样式 */
QDialog {
    background: white;
    border-radius: 12px;
}

/* 列表样式 */
QListWidget {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 4px;
    outline: 0;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #e9ecef;
}

QListWidget::item:selected {
    background: #e7f1ff;
    color: #0d6efd;
    border-radius: 4px;
}

/* 进度条样式 */
QProgressBar {
    border: 1px solid #ced4da;
    border-radius: 4px;
    background: white;
    text-align: center;
}

QProgressBar::chunk {
    background: #0d6efd;
    border-radius: 2px;
}

/* 侧边栏样式 */
#SidebarWidget {
    background: white;
    border-left: 1px solid #dee2e6;
}

/* 历史记录项样式 */
HistoryItemWidget {
    background: white;
    border-radius: 8px;
    border: 1px solid #e9ecef;
}

/* 滚动条样式 */
QScrollBar:vertical {
    border: none;
    background: #f8f9fa;
    width: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #ced4da;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""

class SplashScreen(QSplashScreen):
    """自定义启动画面类"""
    def __init__(self):
        # 创建一个透明的像素图作为基础
        pixmap = QPixmap(500, 300)
        pixmap.fill(Qt.transparent)
        
        super().__init__(pixmap)
        
        # 设置窗口属性
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建容器
        container = QWidget()
        container.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
            border: 1px solid #e0e0e0;
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 应用图标
        self.icon_label = QLabel()
        icon_pixmap = QPixmap("icons/favi.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        # 应用名称
        self.title_label = QLabel("号角浏览器 Horn Browser")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #0d6efd;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # 版本信息
        self.version_label = QLabel("版本: 3.0 Stable")
        self.version_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        self.version_label.setAlignment(Qt.AlignCenter)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background: #f8f9fa;
            }
            QProgressBar::chunk {
                background: #0d6efd;
                border-radius: 4px;
            }
        """)
        
        # 状态文本
        self.status_label = QLabel("正在启动...")
        self.status_label.setStyleSheet("font-size: 12px; color: #6c757d;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # 添加到布局
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.version_label)
        layout.addSpacing(20)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        
        self.main_layout.addWidget(container)
        
        # 居中显示
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )
    
    def update_progress(self, value, message=None):
        """更新进度条和状态信息"""
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)
        QApplication.processEvents()  # 确保UI更新

class WebEngineView(QWebEngineView):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.iconChanged.connect(self.update_tab_icon)
        self.thumbnail = None  # 用于存储缩略图

    def createWindow(self, type):
        new_view = WebEngineView(self.main_window)
        self.main_window.create_tab(new_view)
        return new_view

    def update_tab_icon(self):
        index = self.main_window.tab_widget.indexOf(self.parent().parent())
        self.main_window.tab_widget.setTabIcon(index, self.icon())
        
    def capture_thumbnail(self):
        """捕获当前网页的缩略图"""
        self.thumbnail = self.grab()

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SidebarWidget")
        self.setMinimumWidth(400)
        self.setMaximumWidth(600)
        
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 顶部控制栏
        control_bar = QWidget()
        control_bar.setStyleSheet("background: #f8f9fa; border-bottom: 1px solid #dee2e6;")
        control_layout = QHBoxLayout(control_bar)
        control_layout.setContentsMargins(12, 8, 12, 8)
        
        self.title_label = QLabel("Horn.Browser Bar")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #0d6efd;")
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px; 
                border: none;
                color: #6c757d;
                background: transparent;
            }
            QPushButton:hover {
                color: #0d6efd;
                background: #e9ecef;
                border-radius: 16px;
            }
        """)
        
        control_layout.addWidget(self.title_label)
        control_layout.addStretch()
        control_layout.addWidget(self.close_btn)
        
        # 网页视图
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl("https://horn-studio.github.io/Horn.Browser_Bar/"))
        
        # 添加到布局
        layout.addWidget(control_bar)
        layout.addWidget(self.web_view, 1)

class HistoryItemWidget(QWidget):
    def __init__(self, icon, title, url, visit_time, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border-radius: 8px;")
        
        # 设置布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # 网站图标
        self.icon_label = QLabel()
        self.icon_label.setPixmap(icon.pixmap(32, 32))
        self.icon_label.setFixedSize(32, 32)
        
        # 网站信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; color: #212529;")
        
        self.url_label = QLabel(url)
        self.url_label.setStyleSheet("color: #6c757d; font-size: 11px;")
        
        self.time_label = QLabel(visit_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.time_label.setStyleSheet("color: #868e96; font-size: 10px;")
        
        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.url_label)
        info_layout.addWidget(self.time_label)
        
        # 添加到主布局
        layout.addWidget(self.icon_label)
        layout.addLayout(info_layout, 1)
        
        # 设置悬停效果
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            HistoryItemWidget {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
            HistoryItemWidget:hover {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
            }
        """)

class HistoryDialog(QDialog):
    def __init__(self, history_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("浏览历史")
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon("icons/recent.png"))
        
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # 标题栏
        title_layout = QHBoxLayout()
        title_label = QLabel("浏览历史")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0d6efd;")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 搜索框
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("搜索历史记录...")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 14px;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_history)
        
        # 历史记录列表
        self.history_list = QListWidget()
        self.history_list.setIconSize(QSize(32, 32))
        self.history_list.setSelectionMode(QListWidget.SingleSelection)
        self.history_list.setSpacing(8)
        self.history_list.setStyleSheet("border: none;")
        self.history_list.itemDoubleClicked.connect(self.open_history_item)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清除历史记录")
        self.clear_btn.setIcon(QIcon("icons/clear.png"))
        self.clear_btn.setStyleSheet("background: #fff3cd; color: #856404;")
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.setStyleSheet("background: #e2e3e5; color: #383d41;")
        
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        # 添加到主布局
        layout.addLayout(title_layout)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.history_list, 1)
        layout.addLayout(button_layout)
        
        # 连接信号
        self.close_btn.clicked.connect(self.close)
        self.clear_btn.clicked.connect(self.clear_history)
        
        # 加载历史数据
        self.history_data = history_data
        self.load_history()
    
    def load_history(self):
        """加载历史记录到列表"""
        self.history_list.clear()
        for item in reversed(self.history_data):
            icon = item.get('icon', QApplication.style().standardIcon(QStyle.SP_FileIcon))
            title = item.get('title', '无标题')
            url = item.get('url', '')
            visit_time = item.get('visit_time', datetime.now())
            
            list_item = QListWidgetItem()
            list_item.setData(Qt.UserRole, url)  # 保存URL数据
            
            # 创建自定义小部件
            widget = HistoryItemWidget(icon, title, url, visit_time)
            list_item.setSizeHint(widget.sizeHint())
            
            self.history_list.addItem(list_item)
            self.history_list.setItemWidget(list_item, widget)
    
    def filter_history(self, text):
        """过滤历史记录"""
        text = text.lower()
        for i in range(self.history_list.count()):
            item = self.history_list.item(i)
            widget = self.history_list.itemWidget(item)
            match = text in widget.title_label.text().lower() or text in widget.url_label.text().lower()
            item.setHidden(not match)
    
    def open_history_item(self, item):
        """打开选中的历史记录"""
        url = item.data(Qt.UserRole)
        if url:
            self.parent().current_webview().load(QUrl(url))
            self.accept()
    
    def clear_history(self):
        """清除所有历史记录"""
        reply = QMessageBox.question(self, "确认清除", 
                                    "确定要清除所有历史记录吗？此操作不可撤销！",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history_data = []
            self.load_history()
            self.parent().save_history()

class MainWindow(QMainWindow):
    def __init__(self, splash=None):
        super().__init__()
        self.setWindowTitle("号角浏览器 - Horn Browser")
        self.setWindowIcon(QIcon('icons/favi.png'))
        self.resize(1366, 760)
        self.home_url = "https://horn-studio.github.io/Horn.Search-Plus/"
        
        # 保存启动画面引用
        self.splash = splash
        
        # 更新启动画面状态
        if self.splash:
            self.splash.update_progress(20, "初始化应用...")
        
        # 设置应用样式
        self.setStyleSheet(APP_STYLESHEET)
        
        # 更新启动画面状态
        if self.splash:
            self.splash.update_progress(30, "加载历史记录...")
        
        # 初始化历史记录
        self.history_file = "recent.txt"
        self.history = self.load_history()
        
        # 更新启动画面状态
        if self.splash:
            self.splash.update_progress(50, "配置外部下载...")
        
        # 配置外部下载处理
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_external_download)

        # 创建主布局
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        
        # 使用水平布局管理主区域和侧边栏
        self.main_layout = QHBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 初始化标签页区域
        self.tab_area = QWidget()
        self.tab_layout = QVBoxLayout(self.tab_area)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        
        # 初始化标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_url_bar)
        
        # 添加标签页悬停预览功能
        self.tab_widget.tabBar().setMouseTracking(True)
        self.tab_widget.tabBar().installEventFilter(self)
        self.tab_preview = None
        
        self.tab_layout.addWidget(self.tab_widget)
        self.main_layout.addWidget(self.tab_area, 1)  # 主区域占据大部分空间
        
        # 初始化侧边栏（初始不可见）
        self.sidebar = Sidebar()
        self.sidebar.close_btn.clicked.connect(self.toggle_sidebar)
        self.sidebar.setVisible(False)
        self.main_layout.addWidget(self.sidebar, 0)  # 侧边栏初始宽度为0

        # 更新启动画面状态
        if self.splash:
            self.splash.update_progress(70, "初始化工具栏...")
        
        # 初始化工具栏
        self.init_toolbar()

        # 更新启动画面状态
        if self.splash:
            self.splash.update_progress(90, "创建初始标签页...")
        
        # 创建初始标签页
        self.create_tab()

        # 更新启动画面状态
        if self.splash:
            self.splash.update_progress(100, "准备就绪...")
            
    def eventFilter(self, obj, event):
        """事件过滤器，用于处理标签页悬停预览"""
        if obj == self.tab_widget.tabBar():
            if event.type() == QEvent.MouseMove:
                # 获取鼠标位置下的标签索引
                pos = event.pos()
                index = self.tab_widget.tabBar().tabAt(pos)
                if index >= 0:
                    self.show_tab_preview(index)
                else:
                    self.hide_tab_preview()
            elif event.type() == QEvent.Leave:
                self.hide_tab_preview()
                
        return super().eventFilter(obj, event)
        
    def show_tab_preview(self, index):
        """显示标签页预览"""
        # 获取标签页的webview
        webview = self.tab_widget.widget(index).findChild(QWebEngineView)
        if webview:
            # 如果webview有缓存的缩略图，使用缓存
            if webview.thumbnail:
                pixmap = webview.thumbnail
            # 否则尝试获取实时截图
            else:
                pixmap = webview.grab()
                # 保存为缩略图缓存
                webview.thumbnail = pixmap
            
            # 调整预览大小
            preview_size = QSize(400, 300)
            scaled_pixmap = pixmap.scaled(preview_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # 创建或更新预览窗口
            if self.tab_preview is None:
                self.tab_preview = QLabel(self)
                self.tab_preview.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
                self.tab_preview.setStyleSheet("""
                    background: white;
                    border: 1px solid #ced4da;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                """)
                self.tab_preview.setAlignment(Qt.AlignCenter)
            
            self.tab_preview.setPixmap(scaled_pixmap)
            
            # 获取鼠标位置并显示预览
            cursor_pos = QCursor.pos()
            self.tab_preview.move(cursor_pos + QPoint(20, 20))
            self.tab_preview.adjustSize()
            self.tab_preview.show()
            
    def hide_tab_preview(self):
        """隐藏标签页预览"""
        if self.tab_preview:
            self.tab_preview.hide()

    def init_toolbar(self):
        toolbar = QToolBar("导航栏")
        toolbar.setIconSize(QSize(28, 28))
        toolbar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea, toolbar)

        # 导航按钮
        self.back_btn = QAction(QIcon('icons/back.png'), '返回', self)
        self.forward_btn = QAction(QIcon('icons/forward.png'), '前进', self)
        self.refresh_btn = QAction(QIcon('icons/refresh.png'), '刷新', self)
        self.home_btn = QAction(QIcon('icons/home.png'), '主页', self)
        self.ai_btn = QAction(QIcon('icons/ai.png'), 'Horn.Browser Bar', self)
        self.history_btn = QAction(QIcon('icons/recent.png'), '历史记录', self)

        # 地址栏容器
        address_container = QWidget()
        address_layout = QHBoxLayout(address_container)
        address_layout.setContentsMargins(0, 0, 0, 0)
        address_layout.setSpacing(6)

        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址或搜索内容...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # 外部打开按钮
        self.external_btn = QToolButton()
        self.external_btn.setIcon(QIcon('icons/openinother.png'))
        self.external_btn.setToolTip("在外部浏览器打开")
        self.external_btn.setStyleSheet("border-radius: 16px;")
        self.external_btn.clicked.connect(self.open_external)

        # 将组件添加到地址栏
        address_layout.addWidget(self.url_bar, 1)  # 地址栏占据剩余空间
        address_layout.addWidget(self.external_btn)

        # 添加工具栏组件
        toolbar.addAction(self.back_btn)
        toolbar.addAction(self.forward_btn)
        toolbar.addAction(self.refresh_btn)
        toolbar.addAction(self.home_btn)
        toolbar.addSeparator()
        toolbar.addWidget(address_container)
        toolbar.addSeparator()
        toolbar.addAction(self.ai_btn)
        toolbar.addAction(self.history_btn)

        # 连接信号
        self.back_btn.triggered.connect(lambda: self.current_webview().back())
        self.forward_btn.triggered.connect(lambda: self.current_webview().forward())
        self.refresh_btn.triggered.connect(lambda: self.current_webview().reload())
        self.home_btn.triggered.connect(self.go_home)
        self.ai_btn.triggered.connect(self.toggle_sidebar)
        self.history_btn.triggered.connect(self.show_history)

    def toggle_sidebar(self):
        """切换侧边栏的显示状态"""
        self.sidebar.setVisible(not self.sidebar.isVisible())
        # 根据侧边栏状态调整按钮文本
        self.ai_btn.setText("关闭侧边栏" if self.sidebar.isVisible() else "打开侧边栏")

    def create_tab(self, webview=None):
        webview = webview or WebEngineView(self)
        if not webview.url().isValid():
            webview.load(QUrl(self.home_url))

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)

        tab_index = self.tab_widget.addTab(container, "新标签页")
        self.tab_widget.setTabIcon(tab_index, webview.icon())
        self.tab_widget.setCurrentIndex(tab_index)

        # 连接信号
        webview.urlChanged.connect(lambda url: self.update_url_bar(url))
        webview.titleChanged.connect(lambda title: self.update_tab_title(tab_index, title))
        webview.iconChanged.connect(lambda: self.update_tab_icon(tab_index, webview.icon()))
        webview.loadFinished.connect(self.record_history)  # 记录历史
        
        # 当页面加载完成时捕获缩略图
        webview.loadFinished.connect(lambda: self.capture_thumbnail(webview))

    def capture_thumbnail(self, webview):
        """捕获网页缩略图"""
        # 使用定时器延迟捕获，确保页面完全渲染
        QTimer.singleShot(500, lambda: webview.capture_thumbnail())

    def handle_external_download(self, download_request):
        """处理下载请求，使用外部浏览器打开下载链接"""
        download_url = download_request.url().toString()
        
        # 取消内置下载
        download_request.cancel()
        
        # 使用外部浏览器打开下载链接
        try:
            webbrowser.open(download_url)
            self.statusBar().showMessage(f"已在外部浏览器中打开下载链接: {download_url}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "外部下载失败", 
                               f"无法在外部浏览器中打开下载链接:\n{str(e)}")
    
    def record_history(self, success):
        """记录访问历史"""
        if not success:
            return
            
        webview = self.sender()
        if not webview:
            return
            
        url = webview.url().toString()
        title = webview.title()
        icon = webview.icon()
        
        # 检查是否已记录相同URL
        existing_entry = next((item for item in self.history if item.get('url') == url), None)
        
        # 如果已存在，更新访问时间和标题
        if existing_entry:
            existing_entry['visit_time'] = datetime.now()
            existing_entry['title'] = title
        else:
            # 添加新记录
            self.history.append({
                'url': url,
                'title': title,
                'visit_time': datetime.now(),
                'icon': icon
            })
        
        # 限制历史记录数量
        if len(self.history) > 100:
            self.history = self.history[-100:]
            
        # 保存历史记录
        self.save_history()

    def save_history(self):
        """保存历史记录到文件"""
        try:
            # 准备可序列化的历史数据
            serializable_history = []
            for item in self.history:
                serializable_item = item.copy()
                # 将datetime转换为字符串
                if isinstance(serializable_item.get('visit_time'), datetime):
                    serializable_item['visit_time'] = serializable_item['visit_time'].isoformat()
                # 转换图标为Base64
                if isinstance(serializable_item.get('icon'), QIcon):
                    pixmap = serializable_item['icon'].pixmap(32, 32)
                    buffer = QBuffer()
                    buffer.open(QBuffer.ReadWrite)
                    pixmap.save(buffer, "PNG")
                    base64_data = buffer.data().toBase64().data().decode()
                    serializable_item['icon'] = base64_data
                serializable_history.append(serializable_item)
            
            with open(self.history_file, 'w') as f:
                json.dump(serializable_history, f, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {str(e)}")

    def load_history(self):
        """从文件加载历史记录"""
        if not os.path.exists(self.history_file):
            return []
            
        try:
            with open(self.history_file, 'r') as f:
                history_data = json.load(f)
                
            # 转换回原始格式
            restored_history = []
            for item in history_data:
                # 转换时间字符串为datetime
                if 'visit_time' in item:
                    item['visit_time'] = datetime.fromisoformat(item['visit_time'])
                # 转换Base64为图标
                if 'icon' in item and isinstance(item['icon'], str):
                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray.fromBase64(item['icon'].encode()))
                    item['icon'] = QIcon(pixmap)
                restored_history.append(item)
                
            return restored_history
        except Exception as e:
            print(f"加载历史记录失败: {str(e)}")
            return []

    def show_history(self):
        """显示历史记录对话框"""
        dialog = HistoryDialog(self.history, self)
        dialog.exec()
        
    def update_tab_icon(self, index, icon):
        self.tab_widget.setTabIcon(index, icon)

    def update_tab_title(self, index, title):
        self.tab_widget.setTabText(index, title[:15] + "..." if len(title) > 15 else title)

    def current_webview(self):
        return self.tab_widget.currentWidget().findChild(QWebEngineView)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def navigate_to_url(self):
        url = QUrl.fromUserInput(self.url_bar.text())
        if url.scheme() == "":
            url.setScheme("http")
        self.current_webview().load(url)

    def update_url_bar(self, qurl=None):
        qurl = qurl or self.current_webview().url()
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def go_home(self):
        self.current_webview().load(QUrl(self.home_url))

    def open_external(self):
        current_url = self.url_bar.text()
        if current_url:
            try:
                webbrowser.open(current_url)
                self.statusBar().showMessage(f"已在外部浏览器中打开: {current_url}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "打开失败", f"无法打开外部浏览器:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建并显示启动画面
    splash = SplashScreen()
    splash.show()
    
    # 更新启动画面状态
    splash.update_progress(10, "检查图标...")
    
    # 检查图标目录
    if not os.path.exists("icons"):
        os.makedirs("icons")
        # 创建默认图标文件
        QMessageBox.warning(None, "图标缺失", "请将图标文件放入 icons 目录")
    
    # 检查图标是否存在，不存在则创建默认图标
    icons_to_check = [
        ('favi.png', Qt.blue, "F"),
        ('ai.png', Qt.green, "AI"),
        ('recent.png', Qt.red, "H"),
        ('back.png', Qt.darkBlue, "<"),
        ('forward.png', Qt.darkBlue, ">"),
        ('refresh.png', Qt.darkBlue, "↻"),
        ('home.png', Qt.darkBlue, "⌂"),
        ('openinother.png', Qt.darkGray, "↗"),
        ('close.png', Qt.red, "×"),
        ('clear.png', Qt.red, "C")
    ]
    
    for icon_name, color, text in icons_to_check:
        icon_path = f"icons/{icon_name}"
        if not os.path.exists(icon_path):
            # 创建默认图标
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 绘制圆形背景
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 32, 32)
            
            # 绘制文本
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
            
            painter.end()
            pixmap.save(icon_path)
    
    # 更新启动画面状态
    splash.update_progress(15, "创建主窗口...")
    
    # 创建主窗口并传入启动画面
    browser = MainWindow(splash)
    
    # 关闭启动画面并显示主窗口
    splash.finish(browser)
    splash.deleteLater()
    
    browser.show()
    sys.exit(app.exec())