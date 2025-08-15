import sys
import os
import webbrowser
from datetime import datetime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineDownloadRequest

class DownloadItem(QWidget):
    def __init__(self, download, parent=None):
        super().__init__(parent)
        self.download = download
        self.start_time = datetime.now()
        self.received = 0
        self.total = 0

        layout = QHBoxLayout(self)
        self.name_label = QLabel(download.downloadFileName())
        self.progress = QProgressBar()
        self.speed_label = QLabel("0 KB/s")
        self.pause_btn = QPushButton("暂停")

        layout.addWidget(self.name_label, 4)
        layout.addWidget(self.progress, 4)
        layout.addWidget(self.speed_label, 2)
        layout.addWidget(self.pause_btn, 1)

        download.receivedBytesChanged.connect(self.update_received)
        download.totalBytesChanged.connect(self.update_total)
        download.stateChanged.connect(self.update_button_state)
        download.finished.connect(self.download_finished)
        self.pause_btn.clicked.connect(self.toggle_pause)

    def toggle_pause(self):
        if self.download.state() == QWebEngineDownloadRequest.DownloadState.Paused:
            self.download.resume()
        else:
            self.download.pause()

    def update_received(self, bytes_received):
        self.received = bytes_received
        self.update_progress()

    def update_total(self, bytes_total):
        self.total = bytes_total
        self.progress.setMaximum(bytes_total)

    def update_progress(self):
        if self.total == 0:
            return

        elapsed = (datetime.now() - self.start_time).total_seconds()
        speed = self.received / elapsed if elapsed > 0 else 0
        self.speed_label.setText(f"{speed/1024:.1f} KB/s")
        self.progress.setValue(self.received)

    def download_finished(self):
        self.pause_btn.setEnabled(False)
        self.speed_label.setText("完成")

    def update_button_state(self, state):
        self.pause_btn.setText("继续" if state == QWebEngineDownloadRequest.DownloadState.Paused else "暂停")

class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("下载管理器")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.download_layout = QVBoxLayout(self.content)
        
        scroll.setWidget(self.content)
        layout.addWidget(scroll)

    def add_download(self, download):
        item = DownloadItem(download)
        self.download_layout.addWidget(item)

class WebEngineView(QWebEngineView):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.iconChanged.connect(self.update_tab_icon)

    def createWindow(self, type):
        new_view = WebEngineView(self.main_window)
        self.main_window.create_tab(new_view)
        return new_view

    def update_tab_icon(self):
        index = self.main_window.tab_widget.indexOf(self.parent().parent())
        self.main_window.tab_widget.setTabIcon(index, self.icon())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("号角浏览器_Horn.Browser")
        self.setWindowIcon(QIcon('icons/favi.png'))
        self.resize(1600, 900)
        self.home_url = "https://horn-studio.github.io/Horn.Search-Plus/"

        # 初始化下载管理器
        self.download_manager = DownloadManager()

        # 初始化标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tab_widget)

        # 初始化工具栏
        self.init_toolbar()

        # 配置下载
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

        # 创建初始标签页
        self.create_tab()

    def init_toolbar(self):
        toolbar = QToolBar("导航栏")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.BottomToolBarArea, toolbar)

        # 导航按钮
        self.back_btn = QAction(QIcon('icons/back.png'), '返回', self)
        self.forward_btn = QAction(QIcon('icons/forward.png'), '前进', self)
        self.refresh_btn = QAction(QIcon('icons/refresh.png'), '刷新', self)
        self.home_btn = QAction(QIcon('icons/home.png'), '主页', self)
        self.download_btn = QAction(QIcon('icons/download.png'), '下载管理器', self)

        # 地址栏容器
        address_container = QWidget()
        address_layout = QHBoxLayout(address_container)
        address_layout.setContentsMargins(0, 0, 0, 0)

        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # 外部打开按钮
        self.external_btn = QToolButton()
        self.external_btn.setIcon(QIcon('icons/openinother.png'))
        self.external_btn.setToolTip("在外部浏览器打开")
        self.external_btn.clicked.connect(self.open_external)

        # 将组件添加到地址栏
        address_layout.addWidget(self.url_bar)
        address_layout.addWidget(self.external_btn)

        # 添加工具栏组件
        toolbar.addAction(self.back_btn)
        toolbar.addAction(self.forward_btn)
        toolbar.addAction(self.refresh_btn)
        toolbar.addAction(self.home_btn)
        toolbar.addSeparator()
        toolbar.addWidget(address_container)
        toolbar.addSeparator()
        toolbar.addAction(self.download_btn)

        # 连接信号
        self.back_btn.triggered.connect(lambda: self.current_webview().back())
        self.forward_btn.triggered.connect(lambda: self.current_webview().forward())
        self.refresh_btn.triggered.connect(lambda: self.current_webview().reload())
        self.home_btn.triggered.connect(self.go_home)
        self.download_btn.triggered.connect(self.download_manager.show)

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

        webview.urlChanged.connect(lambda url: self.update_url_bar(url))
        webview.titleChanged.connect(lambda title: self.update_tab_title(tab_index, title))
        webview.iconChanged.connect(lambda: self.update_tab_icon(tab_index, webview.icon()))

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

    def handle_download(self, download):
        desktop = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        filename = download.suggestedFileName()
        
        download.setDownloadDirectory(desktop)
        download.setDownloadFileName(filename)
        download.accept()
        self.download_manager.add_download(download)

    def open_external(self):
        current_url = self.url_bar.text()
        if current_url:
            try:
                webbrowser.open(current_url)
            except Exception as e:
                QMessageBox.critical(self, "打开失败", f"无法打开外部浏览器:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 检查图标目录
    if not os.path.exists("icons"):
        os.makedirs("icons")
        QMessageBox.warning(None, "图标缺失", "请将图标文件放入 icons 目录")

    browser = MainWindow()
    browser.show()
    sys.exit(app.exec())